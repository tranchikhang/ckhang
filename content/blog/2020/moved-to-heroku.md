---
title: "Moved my site to Heroku"
date: 2020-07-05
summary: ""
draft: true
---

I was thinking about moving to Heroku a few weeks ago. My site has been running on Vultr cheapest plan ($3.5 per month) about half year now. I never had really any issue with Vultr, it just that I don't use my site that much, and Heroku free tier should be enough for my needs.


The process was easier than I thought. I just need to:
* Register an account.
* Create an app on Heroku, I can do it directly on their site.
* Connect to my Github repo in a few clicks.
* Create a [Procfile](https://devcenter.heroku.com/articles/procfile) then edit some code to change module path.
* Go to deploy page, "Manual deploy" section, set the branch and click "Deploy branch" (I haven't tried the Automatic deploys feature yet).

That's all, my site is online now.