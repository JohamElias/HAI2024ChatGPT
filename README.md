# Japanese Language Learning Bot

This bot is designed to assist Japanese language learners aiming to pass the N5 level of the Japanese Language Proficiency Test (JLPT). By leveraging the APIs of ChatGPT and Claude, it offers a range of interactive features to enhance the learning experience.

![image](https://github.com/JohamElias/HAI2024ChatGPT/assets/104042919/3a42b805-c392-4505-9781-33ef8888ed75)

- **PDF Charts generation by AI**:

![image](https://github.com/JohamElias/HAI2024ChatGPT/assets/104042919/c3dcce19-1241-403d-b190-02c2a313a1a8)

## Features

- **Socket Implementation**: For real-time interaction without the need for constant page reloading or polling.
- **Voice Recognition**: Utilizes the `SpeechRecognition` API to allow users to interact with the bot using their voice.
- **Speech Output**: Capable of responding to user inputs with voice replies through the `speechSynthesis` API, making the learning process more engaging and interactive.
- **Multilingual Support**: Accepts input in both Japanese and Spanish, catering to a wider range of learners.
- **Custom PDF Generation**: Generates personalized study materials in PDF format, powered by AI. Users can request materials on specific topics of interest to them, facilitating targeted study sessions.

## Getting Started

To get started with this bot, clone the repository to your local machine:

```bash
git clone https://github.com/JohamElias/HAI2024ChatGPT.git
```
## Usage

Here are some basic commands to get you started:

- To start a conversation or ask a question, simply say "Hello" or ask your question in Japanese or Spanish.
- To request study materials, specify the topic you're interested in, for example, "Generate study materials for Kanji."

Remember, the bot is designed to assist with language learning, so feel free to experiment with different types of queries or requests related to the Japanese language.

## Opportunities for Improvement

While the bot provides a comprehensive toolset for learners of the Japanese language, there are several areas identified for potential improvement:

- **Visibility of System Status**: Currently, there is a lack of indicators for when the API is processing a request, leading to uncertainty about the bot's status. Implementing a loading indicator or similar feedback mechanism would enhance user experience by making the system's status visible.

- **Handling of Lengthy Responses**: When the bot generates a particularly long response, the speech synthesis might cut off before completing, and the bot may not accept further input immediately. This could be addressed by breaking down responses into smaller segments or by improving the management of speech synthesis processes.

- **Bilingual Responses**: To aid in language comprehension and pronunciation learning, it would be beneficial for the bot to provide responses in both Japanese and its Spanish translation. This feature would help students better understand and learn the pronunciation of Japanese phrases and sentences.

These improvements aim to enhance the usability and educational value of the bot. Contributions toward addressing these challenges are highly welcome.


## Contributing

This project is a fork from Alexis Mesenses's original work. Contributions are welcome, and any help to extend the functionality, fix bugs, or improve the documentation would be greatly appreciated. Please feel free to submit pull requests or open issues to discuss potential changes or additions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
