---
layout: post
title:  "Unix Lessons Learned"
date:   2021-07-26 21:17:46 +0200
categories: devops rest
---

# What is a GitHub App?
As stated in [GitHub Docs](https://docs.github.com/en/developers/apps/getting-started-with-apps/about-apps), GitHub apps are essentially integrations with the GitHub APIs that allow you to create custom functionality and integrate it into your workflow such that it is performed automatically. These integrations can also be shared with others on GitHub Marketplace. 

GitHub Apps are the officially recommended way to integrate with GitHub because they offer much more granular permissions to access data compared to OAuth Apps.

f you are using your app with GitHub Actions and want to modify workflow files, you must authenticate on behalf of the user with an OAuth token that includes the `workflow` scope. The user must have admin or write permission to the repository that contains the workflow file. 

A GitHub App acts on its own behalf, taking actions via the API directly using its own identity, which means you don't need to maintain a bot or service account as a separate user.

GitHub Apps can be installed directly on organizations and user accounts and granted access to specific repositories. They come with built-in webhooks and narrow, specific permissions. When you set up your GitHub App, you can select the repositories you want it to access. For example, you can set up an app called `MyGitHub` that writes issues in the `octocat` repository and only the octocat repository. To install a GitHub App, you must be an organization owner or have admin permissions in a repository.

# Building Our First API
[GitHub Docs](https://docs.github.com/en/developers/apps/guides/using-the-github-api-in-your-app) describe how to use the GitHub API in our app, and how to set up your app to listen for events and use the Octokit library to perform REST API operations. 

This project will walk you through the following:
* Programming your app to listen for events
* Using the Octokit.rb library to do REST API operations

## Prerequisites

### Webhooks
Webhooks allow to build or set up integrations such as GitHub Apps which subscribe to certain events on GitHub.com. When one of those events is triggered, GitHub sends an HTTP POST payload to the webhook's configured URL. Webhooks can be used for anything from updating an external issue tracker to triggering CI builds to deploying to the production server. 

Webhooks can be installed on an organization, a specific repository, or a GitHub App. Once installed, the webhook will be sent each time one or more subscribed events occurs.

GitHub allows to create up to 20 webhooks for each event on each installation target (specific organization or specific repository).

When configuring a webhook, you can use the UI or API to choose which **events** will send you payloads, i.e., you subscribe to specific events. You can also subscribe to all current and future events. By default, webhooks are only subscribed to the push event. You can change the list of subscribed events anytime.

Each **event** corresponds to a certain set of actions that can happen to your organization and/or repository. For example, if you subscribe to the `issues` event you'll receive detailed payloads every time an issue is opened, closed, labeled, etc.

Here's a [complete list of available webhook events](https://docs.github.com/en/developers/webhooks-and-events/webhook-events-and-payloads) and their payloads.


### REST APIs
[GitHub REST APIs](https://docs.github.com/en/rest) can be used to create calls to get the data you need to integrate with GitHub. Examples can be found [here](https://docs.github.com/en/rest/overview/resources-in-the-rest-api). In its current version, GitHub apparently [uses GraphQL API](https://docs.github.com/en/rest/overview/resources-in-the-rest-api). 

Here's a [Getting started with GitHub APIs guide](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api).


### Sinatra
[Sinatra](http://sinatrarb.com/) is a DSL for quickly creating web applications in Ruby with minimal effort. Here is a short [getting started with Sinatra](http://sinatrarb.com/intro.html). 



## Building an App
First, clone [this repository](https://github.com/github-developer/using-the-github-api-in-your-app).

```shell
paul@terminus:~/Temp$ git clone https://github.com/github-developer/using-the-github-api-in-your-app.git
Cloning into 'using-the-github-api-in-your-app'...
remote: Enumerating objects: 85, done.
remote: Counting objects: 100% (7/7), done.
remote: Compressing objects: 100% (7/7), done.
remote: Total 85 (delta 2), reused 0 (delta 0), pack-reused 78
Unpacking objects: 100% (85/85), done.
Checking connectivity... done.
paul@terminus:~/Temp$ cd using-the-github-api-in-your-app/
paul@terminus:~/Temp/using-the-github-api-in-your-app$ ls
config.ru  Gemfile  Gemfile.lock  README.md  server.rb  template_server.rb
paul@terminus:~/Temp/using-the-github-api-in-your-app$
```

Inside the directory, you'll find a `template_server.rb` file with the template code you'll use in this quickstart and a `server.rb` file with the completed project code.

Next, you need to [follow these steps](https://docs.github.com/en/developers/apps/getting-started-with-apps/setting-up-your-development-environment-to-create-a-github-app) to configure and run the template_server.rb app server. GitHub Apps require some setup steps to manage webhook events and connect the app registration on GitHub to your code.

By the end of this guide you'll have registered a GitHub App and set up a web server to receive webhook events. You'll learn how to use a tool called Smee to capture webhook payloads and forward them to your local development environment. The template app you'll configure in this section won't do anything special yet, but it will serve as a framework you can use to start writing app code using the API or complete other [quickstart guides](https://docs.github.com/en/apps/quickstart-guides). 

Here are the steps you'll take to configure the template GitHub App:

1. Start a new Smee channel
2. Register a new GitHub App
3. Save your private key and App ID
4. Prepare the runtime environment
5. Review the GitHub App template code
6. Start the server
7. Install the app on your account


To help GitHub send webhooks to your local machine without exposing it to the internet, you can use a tool called Smee. First, go to https://smee.io and click Start a new channel. If you're already comfortable with other tools that expose your local machine to the internet like ngrok or localtunnel, feel free to use those.

Starting a new Smee channel creates a unique domain where GitHub can send webhook payloads. You'll need to know this domain for the next step. 

Now see the Docker image and **find out how to pass the Smee URL using an environment variable**!!!

















# Building GitHub App

https://docs.github.com/en/developers/apps/guides/using-the-github-api-in-your-app


listen for events and use the Octokit library to perform REST API operations.


Webhooks

Webhooks allow you to build or set up integrations, such as GitHub Apps or OAuth Apps, which subscribe to certain events on GitHub.com. When one of those events is triggered, we'll send a HTTP POST payload to the webhook's configured URL.

Each event corresponds to a certain set of actions that can happen to your organization and/or repository. For example, if you subscribe to the issues event you'll receive detailed payloads every time an issue is opened, closed, labeled, etc.

When you create a new webhook, we'll send you a simple ping event to let you know you've set up the webhook correctly.


GitHub REST API

https://docs.github.com/en/rest


Sinatra

http://sinatrarb.com/


Setting up Development Environment for GitHub Apps

https://docs.github.com/en/apps/quickstart-guides/setting-up-your-development-environment

GitHub Apps require some setup steps to manage webhook events and connect the app registration on GitHub to your code.

https://smee.io/ to open a new channel to receive the events. Starting a new Smee channel creates a unique domain where GitHub can send webhook payloads.

The channel is: https://smee.io/cC7EjQHzNcmrF2yI



1. Make It Interesting - grab the reader's attention, but do it in an honest way
2. Make It Relevant - explain your motivation, outline your purpose
3. Make It Relatable - build on more familiar concepts in small steps
4. Make It Clear, Concise, and Consistent - remove roadblocks to understanding
5. Make It Memorable - repeat key concepts and end with a bang