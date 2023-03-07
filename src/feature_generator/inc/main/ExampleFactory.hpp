#pragma once

#include "example/Example.hpp"

#include <iostream>

class ExampleFactory
{
    public:
        ExampleFactory();
        ~ExampleFactory() {};

        Example * CreateExample();
};