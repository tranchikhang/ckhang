---
title: "Blog update"
date: 2020-08-28
summary: "Restructured with Hugo and moved to Vercel"
cover: cover.png
draft: true
---

### Why?
I created this site using Python and Flask. Back then, I started working with Python at work, so would be great if I can use it for practice (or so I thought).
I didn't use any CMS, just Flask and some simple logic to manage the content. It works "okay-ish", except:
* Create new content (blog post etc) with HTML is time consuming, especially dealing with syntax highlighting
* I need a server to run my site (I used Vultr at first, then Heroku), but since all of my contents are static, I could save some money using free static hosting service (Heroku is free but still [limited](https://devcenter.heroku.com/articles/free-dyno-hours))

So I searched around for a host which support static file for free, and a Static site generator (Flat-File CMS is a bit overkill in my case).
There are a lot of choices: Jekyll, Lektor, Nikola, MkDocs etc. After playing around with them for a day, I went with [Hugo](https://gohugo.io/)

### Convert my site to Hugo
Installing Hugo was quick, just need to download executable file, add to PATH, and done.
![hugo-install.png](hugo-install.png)
You can follow the [Getting started guide](https://gohugo.io/getting-started/quick-start/) to understand the basic of Hugo.
There are many free templates to choose from [https://themes.gohugo.io/](https://themes.gohugo.io/), installing them is also pretty simple. In my case, I created a new theme since I want to reuse my old site UI.

```cmd
hugo new theme default-theme
```

The newly created theme's folder would look like this:
![new-template-folder.png](new-template-folder.png)

The layouts directory contains all the HTML files that are used for generating HTML. Depends on the page, Hugo automatically chooses which file to use. For example, if you are going to a page that need to render multiple pieces of content (think post list, section list), Hugo will use `list.html`. If you are looking at a single post, then it will be `single.html`.

Partial folder is used to include partial templates (header, footer etc).
Inside these files, you can you [Hugo template language](https://gohugo.io/templates/introduction/) for writing logic and other stuff.

In general, working with template in Hugo is not really hard, you can checkout other tutorials on the Internet. This is the one I used [Let's Create a New Hugo Theme](https://www.pakstech.com/blog/create-hugo-theme/).

After finished creating a default theme, I started converting all my old HTML files to Markdown, which took me a few hours (luckily, I didn't write that much on my old site).

The only problem which took me an hour to figured out is how to create a separate template. I need a different layout for the project page, I cannot use Hugo's default HTML files cause it's not a list nor a single post. The solution turned out is simple: create a `project.html` inside `layouts` folder, then in the Markdown content file, just add `layout: project` at the [front matter](https://gohugo.io/content-management/front-matter/) section.

Let's build the new site:

```cmd
hugo -D
```
And now I can see the new site in the `public` folder.

### Vercel
Vercel is a cloud platform focuses on simplifying deployment. For anyone who didn't know, Vercel is the old now.sh, a product from ZEIT.co. They changed to Vercel in [April 2020](https://vercel.com/blog/zeit-is-now-vercel). For hobby project, they have a free plan which also supports deployment from GitHub, GitLab etc.
![vercel-free-plan.png](vercel-free-plan.png)
When you logged in with your account, you can choose where to import your project.
![vercel-import.png](vercel-import.png)
Vercel also supports template for different frameworks.
![vercel-import-template.png](vercel-import-template.png)

After importing project, Vercel will automatically detect the framework (Hugo in my case).

One problem I had is my site couldn't load CSS correctly, because Vercel was using an older version of Hugo. I had to [manually define](https://vercel.com/guides/deploying-hugo-with-vercel) the version in Vercel config file.

That concludes my migration to Hugo and Vercel.