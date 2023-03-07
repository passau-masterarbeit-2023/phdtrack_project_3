#include "example/Example_perf.hpp"

#include <iostream>
#include <chrono>
#include <string>

void Example_perf::Perf_GenerateRandomNumber()
{
    std::cout << "Start Perf_GenerateRandomNumber" << std::endl;
    
    double nbOfTests = 1000000;
    auto start = std::chrono::high_resolution_clock::now();

    // run and measure
    Example example;
    int randomNumber = 0;
    for (int i = 0; i < nbOfTests; i++)
    {
        randomNumber = example.GenerateRandomNumber(0, 10);
    }

    auto finish = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = finish - start;

    std::cout << "<<<< Total Duration [" << nbOfTests << " tests] : " 
        << elapsed.count() << "s >>>>" << std::endl;
    std::cout << "<<<< Avg Duration : " 
        << (elapsed.count()/nbOfTests)<< "s >>>>" << std::endl;

    std::cout << "End Perf_GenerateRandomNumber" << std::endl;
}