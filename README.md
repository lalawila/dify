![](./images/describe-en.png)
<p align="center">
  <a href="./README.md">English</a> |
  <a href="./README_CN.md">简体中文</a>
</p>

[Website](https://dify.ai) • [Docs](https://docs.dify.ai) • [Twitter](https://twitter.com/dify_ai) • [Discord](https://discord.gg/FngNHpbcY7)

**QiyeGPT** is an easy-to-use LLMOps platform designed to empower more people to create sustainable, AI-native applications. With visual orchestration for various application types, QiyeGPT offers out-of-the-box, ready-to-use applications that can also serve as Backend-as-a-Service APIs. Unify your development process with one API for plugins and datasets integration, and streamline your operations using a single interface for prompt engineering, visual analytics, and continuous improvement.

Applications created with QiyeGPT include:

Out-of-the-box web sites supporting form mode and chat conversation mode
A single API encompassing plugin capabilities, context enhancement, and more, saving you backend coding effort
Visual data analysis, log review, and annotation for applications
QiyeGPT is compatible with Langchain, meaning we'll gradually support multiple LLMs, currently supported:

- GPT 3 (text-davinci-003)
- GPT 3.5 Turbo(ChatGPT)
- GPT-4

## Use Cloud Services

Visit [QiyeGPT.ai](https://dify.ai)

## Install the Community Edition

### System Requirements

Before installing QiyeGPT, make sure your machine meets the following minimum system requirements:

- CPU >= 1 Core
- RAM >= 4GB

### Quick Start

The easiest way to start the QiyeGPT server is to run our [docker-compose.yml](docker/docker-compose.yaml) file. Before running the installation command, make sure that [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) are installed on your machine:

```bash
cd docker
docker-compose up -d
```

After running, you can access the QiyeGPT dashboard in your browser at [http://localhost/install](http://localhost/install) and start the initialization installation process.

### Configuration

If you need to customize the configuration, please refer to the comments in our [docker-compose.yml](docker/docker-compose.yaml) file and manually set the environment configuration. After making the changes, please run 'docker-compose up -d' again.

## Roadmap

Features under development:

- **Datasets**, supporting more datasets, e.g. syncing content from Notion or webpages
We will support more datasets, including text, webpages, and even Notion content. Users can build AI applications based on their own data sources.
- **Plugins**, introducing ChatGPT Plugin-standard plugins for applications, or using QiyeGPT-produced plugins
We will release plugins complying with ChatGPT standard, or QiyeGPT's own plugins to enable more capabilities in applications. 
- **Open-source models**, e.g. adopting Llama as a model provider or for further fine-tuning
We will work with excellent open-source models like Llama, by providing them as model options in our platform, or using them for further fine-tuning.


## Q&A

**Q: What can I do with QiyeGPT?**

A: QiyeGPT is a simple yet powerful LLM development and operations tool. You can use it to build commercial-grade applications, personal assistants. If you want to develop your own applications, LangQiyeGPTGenius can save you backend work in integrating with OpenAI and offer visual operations capabilities, allowing you to continuously improve and train your GPT model.

**Q: How do I use QiyeGPT to "train" my own model?**

A: A valuable application consists of Prompt Engineering, context enhancement, and Fine-tuning. We've created a hybrid programming approach combining Prompts with programming languages (similar to a template engine), making it easy to accomplish long-text embedding or capturing subtitles from a user-input Youtube video - all of which will be submitted as context for LLMs to process. We place great emphasis on application operability, with data generated by users during App usage available for analysis, annotation, and continuous training. Without the right tools, these steps can be time-consuming.

**Q: What do I need to prepare if I want to create my own application?**

A: We assume you already have an OpenAI API Key; if not, please register for one. If you already have some content that can serve as training context, that's great!

**Q: What interface languages are available?**

A: English and Chinese are currently supported, and you can contribute language packs to us.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=langgenius/dify&type=Date)](https://star-history.com/#langgenius/dify&Date)

## Contact Us

If you have any questions, suggestions, or partnership inquiries, feel free to contact us through the following channels:

- Submit an Issue or PR on our GitHub Repo
- Join the discussion in our [Discord](https://discord.gg/FngNHpbcY7) Community
- Send an email to hello@dify.ai

We're eager to assist you and together create more fun and useful AI applications!

## Contributing

To ensure proper review, all code contributions - including those from contributors with direct commit access - must be submitted via pull requests and approved by the core development team prior to being merged.

We welcome all pull requests! If you'd like to help, check out the [Contribution Guide](CONTRIBUTING.md) for more information on how to get started.

## Security

To protect your privacy, please avoid posting security issues on GitHub. Instead, send your questions to security@dify.ai and we will provide you with a more detailed answer.

## Citation

This software uses the following open-source software:

- Chase, H. (2022). LangChain [Computer software]. https://github.com/hwchase17/langchain
- Liu, J. (2022). LlamaIndex [Computer software]. doi: 10.5281/zenodo.1234.

For more information, please refer to the official website or license text of the respective software.

## License

This repository is available under the [QiyeGPT Open Source License](LICENSE).
