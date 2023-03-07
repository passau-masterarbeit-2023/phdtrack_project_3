#pragma once

#include <iostream>
#include <string>
#include <array>

class Example
{
    public:
        Example() {};
        ~Example() {};

        inline void hello()
        {
            std::cout << "[" << nbOfMessages << "] "
                << randomVerse() << std::endl;
            nbOfMessages++;
        }

        int GenerateRandomNumber(int min, int max);

    private:
        static std::array<std::string, 18> const invictusVerses; // declaration
        int nbOfMessages = 0;

        std::string randomVerse();
        
};