#include "ExampleFactory.hpp"
#include "example/Example.hpp"

#include <iostream>

int main(int argc, char** argv)
{
    // print program arguments
    std::cout << "You have entered " << argc
        << " arguments:" << "\n";
  
    for (int i = 0; i < argc; ++i)
    {
        std::cout << "argv[" << i << "]: " << argv[i] << "\n";
    }

    // get number of random verses to print
    int defaultNbOfVerses = 10;
    if (argc > 1)
    {
        defaultNbOfVerses = atoi(argv[1]);
    }

    // use objects and print verses
    ExampleFactory exampleFactory = ExampleFactory();
    Example * example = exampleFactory.CreateExample();

    for(int i = 0; i < defaultNbOfVerses; i++)
    {
        example->hello();
    }

    delete example;
    return 0;
}