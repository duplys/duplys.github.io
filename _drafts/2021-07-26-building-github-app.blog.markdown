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

OK, basically what we want to do is to get rid of the whole setup stuff by building our own Docker image. So the goal is to build a Docker image with the `smee-client` and probably also the `sinatra` app. How to install `smee` is described [here](https://docs.github.com/en/developers/apps/getting-started-with-apps/setting-up-your-development-environment-to-create-a-github-app). I probably need to bind mount the current repository so that I can edit and run the code (i.e., the app).

[Here's](https://docs.docker.com/engine/reference/commandline/run/) how to pass an environment variable to a Docker container. See also [here](https://stackoverflow.com/questions/30494050/how-do-i-pass-environment-variables-to-docker-containers). 

First, you need to create a Smee channel as described [here](https://docs.github.com/en/developers/apps/getting-started-with-apps/setting-up-your-development-environment-to-create-a-github-app). 


OK, run `make` to build the Docker image containing the `smee` client. To start the container, use `make run`. What it does under the surface is to execute the command `docker container run -it --rm -e SMEE_URL='https://smee.io/Ch0Kk0wcNDlwqpn' -p 3000:3000 -v $(CURDIR):/opt/github-app github-app-example`. This command starts the container and passes the value `https://smee.io/Ch0Kk0wcNDlwqpn` in the environment variable `SMEE_URL` and bind mounts the current directory under `/opt/github-app` in the Docker container (which allows us to make changes to the app's source code from the host while running it in the Docker container). 

## Next, register a new GitHub App
[This section in GitHub Docs](https://docs.github.com/en/developers/apps/getting-started-with-apps/setting-up-your-development-environment-to-create-a-github-app#step-2-register-a-new-github-app) shows how to do it.

After creating the app, as [explained here](https://docs.github.com/en/developers/apps/getting-started-with-apps/setting-up-your-development-environment-to-create-a-github-app#step-3-save-your-private-key-and-app-id), you'll need to generate a private key for your app and note the app ID GitHub has assigned your app. 

In my case, the app ID App ID: 129472.

Click on generate private key and store the `.pem` file in the directory where I can find it. In the end, the GitHub private app key, the app identified and the webhook secret go into a file `.env` in the repository -- this file might NEVER be added to the repository itself, so make sure you add `.env` to `.gitignore`.

Once this is done, in the Docker container run:

```shell
root@5fb3ad7073a4:/opt/github-app# smee --url ${SMEE_URL} --path /event_handler --port 3000 &
[1] 501
root@5fb3ad7073a4:/opt/github-app# Forwarding https://smee.io/Ch0Kk0wcNDlwqpn to http://127.0.0.1:3000/event_handler

root@5fb3ad7073a4:/opt/github-app# Connected https://smee.io/Ch0Kk0wcNDlwqpn

root@5fb3ad7073a4:/opt/github-app# bundle exec ruby template_server.rb
/var/lib/gems/2.7.0/gems/sinatra-2.0.4/lib/sinatra/base.rb:1641: warning: Using the last argument as keyword parameters is deprecated; maybe ** should be added to the call
/var/lib/gems/2.7.0/gems/mustermann-1.0.3/lib/mustermann.rb:62: warning: The called method `new' is defined here
/var/lib/gems/2.7.0/gems/mustermann-1.0.3/lib/mustermann/pattern.rb:59: warning: Using the last argument as keyword parameters is deprecated; maybe ** should be added to the call
/var/lib/gems/2.7.0/gems/mustermann-1.0.3/lib/mustermann/regular.rb:22: warning: The called method `initialize' is defined here
/var/lib/gems/2.7.0/gems/sinatra-2.0.4/lib/sinatra/base.rb:1604: warning: Using the last argument as keyword parameters is deprecated; maybe ** should be added to the call
/var/lib/gems/2.7.0/gems/sinatra-2.0.4/lib/sinatra/base.rb:1621: warning: The called method `compile!' is defined here
/var/lib/gems/2.7.0/gems/mustermann-1.0.3/lib/mustermann/pattern.rb:59: warning: Using the last argument as keyword parameters is deprecated; maybe ** should be added to the call
/var/lib/gems/2.7.0/gems/mustermann-1.0.3/lib/mustermann/regexp_based.rb:17: warning: The called method `initialize' is defined here
/var/lib/gems/2.7.0/gems/mustermann-1.0.3/lib/mustermann/ast/compiler.rb:43: warning: Using the last argument as keyword parameters is deprecated; maybe ** should be added to the call
/var/lib/gems/2.7.0/gems/mustermann-1.0.3/lib/mustermann/ast/compiler.rb:49: warning: The called method `pattern' is defined here
/var/lib/gems/2.7.0/gems/faraday-0.15.3/lib/faraday/options.rb:166: warning: Capturing the given block using Proc.new is deprecated; use `&block` instead
/var/lib/gems/2.7.0/gems/faraday-0.15.3/lib/faraday/options.rb:166: warning: Capturing the given block using Proc.new is deprecated; use `&block` instead
/var/lib/gems/2.7.0/gems/faraday-0.15.3/lib/faraday/options.rb:166: warning: Capturing the given block using Proc.new is deprecated; use `&block` instead
/var/lib/gems/2.7.0/gems/faraday-0.15.3/lib/faraday/options.rb:166: warning: Capturing the given block using Proc.new is deprecated; use `&block` instead
/var/lib/gems/2.7.0/gems/faraday-0.15.3/lib/faraday/options.rb:166: warning: Capturing the given block using Proc.new is deprecated; use `&block` instead
/var/lib/gems/2.7.0/gems/faraday-0.15.3/lib/faraday/rack_builder.rb:55: warning: Capturing the given block using Proc.new is deprecated; use `&block` instead
/var/lib/gems/2.7.0/gems/sinatra-2.0.4/lib/sinatra/base.rb:1348: warning: Using the last argument as keyword parameters is deprecated; maybe ** should be added to the call
/var/lib/gems/2.7.0/gems/sinatra-2.0.4/lib/sinatra/base.rb:1359: warning: The called method `add_filter' is defined here
/var/lib/gems/2.7.0/gems/sinatra-2.0.4/lib/sinatra/base.rb:1360: warning: Using the last argument as keyword parameters is deprecated; maybe ** should be added to the call
/var/lib/gems/2.7.0/gems/sinatra-2.0.4/lib/sinatra/base.rb:1621: warning: The called method `compile!' is defined here
[2021-07-31 11:32:04] INFO  WEBrick 1.6.0
[2021-07-31 11:32:04] INFO  ruby 2.7.0 (2019-12-25) [x86_64-linux-gnu]
== Sinatra (v2.0.4) has taken the stage on 3000 for development with backup from WEBrick
[2021-07-31 11:32:04] INFO  WEBrick::HTTPServer#start: pid=512 port=3000
```

Continue [reading here](https://docs.github.com/en/developers/apps/guides/using-the-github-api-in-your-app) to see how to setup the correct permissions in the App's section on GitHub in order to access issues.























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