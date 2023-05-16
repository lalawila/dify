# QiyeGPT PHP SDK

This is the PHP SDK for the QiyeGPT API, which allows you to easily integrate QiyeGPT into your PHP applications.

## Requirements

- PHP 7.2 or later
- Guzzle HTTP client library

## Usage

After installing the SDK, you can use it in your project like this:

```
<?php

require 'vendor/autoload.php';

use YourVendorName\QiyeGPTPHP\QiyeGPTClient;
use YourVendorName\QiyeGPTPHP\CompletionClient;
use YourVendorName\QiyeGPTPHP\ChatClient;

$apiKey = 'your-api-key-here';

$difyClient = new QiyeGPTClient($apiKey);

// Create a completion client
$completionClient = new CompletionClient($apiKey);
$response = $completionClient->create_completion_message($inputs, $query, $response_mode, $user);

// Create a chat client
$chatClient = new ChatClient($apiKey);
$response = $chatClient->create_chat_message($inputs, $query, $user, $response_mode, $conversation_id);

// Fetch application parameters
$response = $difyClient->get_application_parameters($user);

// Provide feedback for a message
$response = $difyClient->message_feedback($message_id, $rating, $user);

// Other available methods:
// - get_conversation_messages()
// - get_conversations()
// - rename_conversation()
```

Replace 'your-api-key-here' with your actual QiyeGPT API key.

## License

This SDK is released under the MIT License.