#include "example/Example_test.hpp"


int Example_test::Test_GenerateRandomNumber()
{
    Example example;

    // test 20 times
    for (int i = 0; i < 30; i++)
    {
        int randomNumber = example.GenerateRandomNumber(0, 10);
        std::cout << "Random number: " << randomNumber << std::endl;
        assert(randomNumber >= 0 && randomNumber <= 10);
    }
    return 0;
}