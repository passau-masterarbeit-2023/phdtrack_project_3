#include "example/Example_perf.hpp"

#include <iostream>

void callSpeedTests();

int main()
{
    callSpeedTests();    
    return 0;
}

void callSpeedTests() {
    std::cout << "----- | Starting Speed Tests | -----" << std::endl;
    std::cout << "------------------------------------" << std::endl;
    std::cout << std::endl;

    Example_perf examplePerf;
    examplePerf.Perf_GenerateRandomNumber();

    std::cout << std::endl;
    std::cout << "------------------------------------" << std::endl;
    std::cout << "------ | End of Speed Tests | ------" << std::endl;
}