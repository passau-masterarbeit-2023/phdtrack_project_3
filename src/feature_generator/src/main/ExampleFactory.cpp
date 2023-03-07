#include "ExampleFactory.hpp"

ExampleFactory::ExampleFactory()
{}

Example * ExampleFactory::CreateExample()
{
    std::cout << "Creating new Example" << std::endl;
    return new Example();
}