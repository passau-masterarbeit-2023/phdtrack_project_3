#include "example/Example.hpp"

// static const vector (here array) initialization outside class: 
// https://stackoverflow.com/questions/12855649/how-can-i-iitialize-a-static-const-vector-that-is-a-class-member-in-c11
// definition needs to be in .cpp file:
std::array<std::string, 18> const Example::invictusVerses = {
    "Invictus",
    "Out of the night that covers me,",  
    "Black as the Pit from pole to pole,",  
    "I thank whatever gods may be", 
    "For my unconquerable soul.", 
    "In the fell clutch of circumstance",
    "I have not winced nor cried aloud.",   
    "Under the bludgeonings of chance",  
    "My head is bloody, but unbowed.",  
    "Beyond this place of wrath and tears", 
    "Looms but the Horror of the shade,",
    "And yet the menace of the years",
    "Finds, and shall find, me unafraid.",
    "It matters not how strait the gate,", 
    "How charged with punishments the scroll,",
    "I am the master of my fate:",
    "I am the captain of my soul.",
    "William Ernest Henley - 1849-1903"
};

/**
 * @brief Generate a random int between min and max (included).
 * 
 * @param min Lower bound (included)
 * @param max Upper bound (included)
 * @return int Random generated integer.
 */
int Example::GenerateRandomNumber(int min, int max)
{
    return (rand() % (max - min + 1)) + min;
}

/**
 * @brief Return a random verse from Invictus, William Ernest Henley.
 * 
 * @return std::string 
 */
std::string Example::randomVerse()
{
    static constexpr int maxMessagesIndex = 
        invictusVerses.size() - 1;
    std::string randomVerse = invictusVerses[
        GenerateRandomNumber(0, maxMessagesIndex)];
    return randomVerse;
}