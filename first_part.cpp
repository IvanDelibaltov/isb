#include <fstream>
#include <iostream>
#include <ctime>
#include <cstdlib>

using namespace std;

string generateBinaryString() {
    srand(time(nullptr));

    string binaryData;
    const int LENGTH = 128;

    for (int counter = 0; counter < LENGTH; ++counter) {
        binaryData += rand() % 2 ? "1" : "0";
    }

    return binaryData;
}

void writeDataToFile(const string& fileName, const string& dataContent) {
    ofstream outputFile(fileName);
    outputFile << dataContent;
    outputFile.close();
}

int executeProgram() {
    string binaryResult = generateBinaryString();
    writeDataToFile("Binary_Output.txt", binaryResult);
    return 0;
}

int main() {
    return executeProgram();
}