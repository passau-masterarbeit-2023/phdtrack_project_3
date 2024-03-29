use crate::{graph_data::GraphData, graph_structs::{Node, ValueNode, KeyNode, SpecialNodeAnnotation}, utils::div_round_up};
use std::path::PathBuf;

pub struct GraphAnnotate {
    pub graph_data: GraphData,

    
}

impl GraphAnnotate {
    pub fn new(
        heap_dump_raw_file_path: PathBuf, 
        pointer_byte_size: usize,
        annotation : bool,
        without_value_nodes : bool,
    ) -> Result<GraphAnnotate, crate::utils::ErrorKind> {
        let graph_data = GraphData::new(heap_dump_raw_file_path, pointer_byte_size, annotation, without_value_nodes)?;
        
        let mut graph_annotate = GraphAnnotate {
            graph_data,
        };
        if annotation {
            graph_annotate.annotate();
        }
        Ok(graph_annotate)
    }

    /// Annotate the graph with data from the JSON file
    /// stored in heap_dump_data
    fn annotate(&mut self) {
        self.annotate_graph_with_key_data();
        self.annotate_graph_with_ssh_struct();
    }

    /// annotate graph with ssh struct
    /// - annotate the value node of the ssh struct as ssh struct node (if we genrate a graph without value nodes, annotate the dtn node as ssh struct node)
    fn annotate_graph_with_ssh_struct(&mut self) {
        {
            // SSH_STRUCT_ADDR
            let mut ssh_struct_addr = self.graph_data.heap_dump_data.as_ref().unwrap().addr_ssh_struct;
            if self.graph_data.no_value_node {
                ssh_struct_addr = self.graph_data.get_parent_dtn_addr(&ssh_struct_addr).unwrap();
            }
            
            self.annotate_node(SpecialNodeAnnotation::SshStructNodeAnnotation(ssh_struct_addr));
        }
        {
            // SESSION_STATE_ADDR
            let mut session_state_addr = self.graph_data.heap_dump_data.as_ref().unwrap().addr_session_state;
            if self.graph_data.no_value_node {
                session_state_addr = self.graph_data.get_parent_dtn_addr(&session_state_addr).unwrap();
            }

            self.annotate_node(SpecialNodeAnnotation::SessionStateNodeAnnotation(session_state_addr));
        }
    }

    /// annotate graph with key data from json file
    /// - aggreagte the value node of the key into a key node
    /// - annotate the key node created as keynode (if we genrate a graph without value nodes, annotate the dtn node as keynode)
    fn annotate_graph_with_key_data(&mut self) {
        let mut annotations = Vec::new();

        let no_value_node = self.graph_data.no_value_node;
        let addr_to_key_data = &self.graph_data.heap_dump_data.as_ref().unwrap().addr_to_key_data;
        // iterate over all the key data
        for (addr, key_data) in addr_to_key_data{
            // get the node at the key_data's address
            let node: Option<&Node> = self.graph_data.addr_to_node.get(addr);
            if node.is_some() && node.unwrap().is_value() {

                // if the node is a ValueNode, then we can annotate it
                // i.e. we create a KeyNode from the Node and its key_data
                let mut aggregated_key: Vec<u8> = Vec::new();

                // get all the ValueNodes that are part of the key
                // WARN: when the key lenght is not a multiple of the block size,
                //      we need to crop the aggregated_key to the real key length
                // WARN: Need to round up the division that determines the number of blocks needed.
                //      Otherwise, we will miss the last block, since it is possible that we only need a fraction of it.
                let block_size = self.graph_data.heap_dump_data.as_ref().unwrap().block_size;
                for i in 0..div_round_up(key_data.len, block_size) {
                    let current_key_block_addr = addr + (i * block_size) as u64;
                    let current_key_block_node: Option<&Node> = self.graph_data.addr_to_node.get(&current_key_block_addr);
                    if current_key_block_node.is_some() {
                        let current_node = current_key_block_node.unwrap();
                        // WARN: it is possible that one the block has been identified as a PointerNode
                        // since we are doing the annotation, we know that it should be a ValueNode.
                        // Do NOT modify the graph, since we are at the annotation stage.
                        // Instead, we just get the value of the ValueNode, and convert the pointer to a row byte array
                        match current_node {
                            Node::ValueNode(_) => {
                                aggregated_key.extend_from_slice(&current_node.get_value().unwrap());
                            },
                            Node::PointerNode(_) => {
                                let pointer_value = current_node.points_to().unwrap();
                                aggregated_key.extend_from_slice(&pointer_value.to_be_bytes());
                            },
                            _ => {
                                // log warning
                                log::warn!(
                                    "current_key_block_node is not a ValueNode nor a PointerNode for addr: {}, for key {}", 
                                    current_key_block_addr, key_data.name
                                );
                                break;
                            },
                        }

                        
                    } else {
                        // log warning
                        log::warn!(
                            "current_key_block_node not found for addr: {}, for key {}", 
                            current_key_block_addr, key_data.name
                        );
                        break;
                    }
                }

                // crop key to real key length
                if aggregated_key.len() > key_data.len {
                    aggregated_key.truncate(key_data.len);
                }
                
                // annotate if the key found in the heap dump is the same as the key found in the json file
                if aggregated_key == key_data.key {
                    let dtn_addr = node.unwrap().get_dtn_addr().unwrap();

                    // replace the ValueNode with a KeyNode
                    let key_node = Node::ValueNode(ValueNode::KeyNode(KeyNode {
                        addr: *addr, // addr of first block of key
                        dtn_addr: dtn_addr, // dtn_addr of first block of key
                        value: node.unwrap().get_value().unwrap(), // first block value of key
                        key: aggregated_key, // found in heap dump, full key (not just the first block)
                        key_data: key_data.clone(), // found in heap dump, key data
                    }));


                    // annotate the dtn node with the key node annotation
                    if no_value_node {
                        annotations.push(SpecialNodeAnnotation::KeyNodeAnnotation(dtn_addr));
                    } else {
                        annotations.push(SpecialNodeAnnotation::KeyNodeAnnotation(*addr));
                    }
                    
                    self.graph_data.addr_to_node.insert(*addr, key_node);
                } else {
                    log::warn!(
                        "key ({}) found in heap dump is not the same as the key found in the json file.  
                        found aggregated_key: {:?}, 
                        expected key_data.key: {:?}", 
                        key_data.name, aggregated_key, key_data.key
                    );
                }

            }
        }

        // annotate the graph with the key node annotations
        for annotation in annotations {
            self.annotate_node(annotation);
        }
    }

    /// annote a node
    fn annotate_node(&mut self, annotation : SpecialNodeAnnotation) {
        self.graph_data.special_node_to_annotation.insert(
            annotation.get_address(),
            annotation,
        );
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::params::{self};
    use crate::graph_structs::{
        Node, 
        ValueNode, 
    };
    use crate::tests::{TEST_GRAPH_DOT_DIR_PATH, TEST_HEAP_DUMP_FILE_NUMBER};

    #[test]
    fn test_annotation() {
        crate::tests::setup();

        let graph_annotate = GraphAnnotate::new(
            params::TEST_HEAP_DUMP_FILE_PATH.clone(), 
            params::BLOCK_BYTE_SIZE,
            true,
            false
        ).unwrap();

        // check that there is the SshStructNodeAnnotation
        let ssh_struct_annotation = graph_annotate.graph_data.special_node_to_annotation.get(&*crate::tests::TEST_SSH_STRUCT_ADDR);
        let ssh_struct_addr = &*crate::tests::TEST_SSH_STRUCT_ADDR;
        
        assert!(ssh_struct_annotation.is_some());
        assert!(matches!(ssh_struct_annotation.unwrap(), SpecialNodeAnnotation::SshStructNodeAnnotation(_)));
        assert!(graph_annotate.graph_data.addr_to_node.get(ssh_struct_addr).is_some());

        let session_state_annotation = graph_annotate.graph_data.special_node_to_annotation.get(&*crate::tests::TEST_SESSION_STATE_ADDR);
        
        assert!(session_state_annotation.is_some());
        assert!(matches!(session_state_annotation.unwrap(), SpecialNodeAnnotation::SessionStateNodeAnnotation(_)));
        // TODO: we have no session state node in the graph ! 
        //let session_state_addr = &*crate::tests::TEST_SESSION_STATE_ADDR;
        // assert!(graph_annotate.graph_data.addr_to_node.get(session_state_addr).is_some());
    }

    #[test]
    fn test_key_annotation() {
        crate::tests::setup();

        let graph_annotate = GraphAnnotate::new(
            params::TEST_HEAP_DUMP_FILE_PATH.clone(), 
            params::BLOCK_BYTE_SIZE,
            true,
            false
        ).unwrap();

        // check that there is at least one KeyNode
        assert!(graph_annotate.graph_data.addr_to_node.values().any(|node| {
            if let Node::ValueNode(ValueNode::KeyNode(_)) = node {
                true
            } else {
                false
            }
        }));

        // check the last key
        let test_key_node = graph_annotate.graph_data.addr_to_node.get(&*crate::tests::TEST_KEY_F_ADDR).unwrap();
        match test_key_node {
            Node::ValueNode(ValueNode::KeyNode(key_node)) => {
                assert_eq!(key_node.key, *crate::tests::TEST_KEY_F_BYTES);
                assert_eq!(key_node.key_data.name, *crate::tests::TEST_KEY_F_NAME);
                assert_eq!(key_node.key_data.len, *crate::tests::TEST_KEY_F_LEN);
            },
            _ => panic!("Node is not a KeyNode"),
        }
    }

    #[test]
    fn test_graph_generation_to_dot() {
        crate::tests::setup();

        use std::path::Path;
        use std::fs::File;
        use std::io::Write;
        
        let graph_annotate = GraphAnnotate::new(
            params::TEST_HEAP_DUMP_FILE_PATH.clone(), 
            params::BLOCK_BYTE_SIZE,
            true,
            false
        ).unwrap();

        // save the graph to a file as a dot file (graphviz)
        let dot_file_name: String = format!("{}test_graph_from_{}.gv", &*TEST_GRAPH_DOT_DIR_PATH, &*TEST_HEAP_DUMP_FILE_NUMBER);
        let dot_file_path = Path::new(dot_file_name.as_str());
        let mut dot_file = File::create(dot_file_path).unwrap();
        dot_file.write_all(format!("{}", graph_annotate.graph_data).as_bytes()).unwrap(); // using the custom formatter

        // check that the value node addresses are kept
        assert!(graph_annotate.graph_data.value_node_addrs.len() > 0);
    }

}