---
title: "Simple Reddit client using Angular (3)"
date: 2020-01-25
summary: "Create a simple Angular application fetching data from Reddit (3)"
keywords: "Angular, TypeScript, Frontend, Framework, JavaScript, HTML, CSS"
tags: ["Angular", "TypeScript", "Frontend", "Framework", "JavaScript", "HTML", "CSS"]
draft: true
---

<a href="/post/2020/simple-reddit-client-web-by-angular-2/">Last post</a>, we restructured the app and added subreddit browsing. In this post, we are going to style the app a bit then implement thread browsing feature.

### Threads list styling
First we will add some style to *thread-list* component.

*src/app/components/thread-list/thread-list.component.html*
```HTML
<div class="list-thread">
    <div class="thread" *ngFor="let thread of threads">
        <div class="title"><a href="{{ thread.permalink }}">{{ thread.linkFlairText }} {{ thread.title }}</a></div>
        <div class="info-1"><span class="points">{{ thread.score }}</span> pts - <span class="comments">{{ thread.num_comments }}</span> comments</div>
        <div class="info-2">{{ thread.createdTime| date:'fullDate' }} by <span class="user">{{ thread.author }}</span></div>
    </div>
</div>
```
*src/app/components/thread-list/thread-list.component.scss*
```CSS
.list-thread {
    display: flex;
    flex-direction: column;
}

.thread {
    margin-bottom: 10px;
}

.thread .title {
    color: #353535;
}

.thread .points {
    color: #E64569;
}

.thread .user {
    color: #3d963b;
}

.thread .comments {
    color: #439ECF;
}
```
We update *thread* model to display more data. *created* time from json data is in second, so we need to multiply by 1000 to get value in millisecond.

*src/app/models/thread.ts*
```TypeScript
export class Thread {
    id: string;
    title: string;
    author: string;
    score: number;
    permalink: string;
    url: string;
    createdTime: Date;
    linkFlairText: string;
    num_comments: number;

    constructor(t: any) {
        this.id = t['id'];
        this.title = t['title'];
        this.author = t['author'];
        this.score = t['score'];
        this.permalink = t['permalink'];
        this.linkFlairText = t['link_flair_text'];
        this.num_comments = t['num_comments'];
        this.createdTime = new Date(t['created'] * 1000);
    }
}
```

Update logic in *common* service follows with modified *thread* model
*src/app/services/common.service.ts*
```TypeScript
getThreads(path: String): Observable&#x3C;any&#x3E; {
    return this.httpClient.get(this.appConfig.baseUrl + path + '.json').pipe(
        map(res => {
            return res['data']['children'].map(thread => {
                return new Thread(thread['data']);
            });
        }
        )
    );
}
```

Run the app to check the result.
```Bash
ng serve
```
![simple-reddit-client-web-by-angular-3-check-1.png](angular-reddit-3-check-1.png)
### Top navigation
Next step, we will create a navigation bar, which appears on top in every pages.
```Bash
ng generate component components/navbar
```
*src/app/components/navbar/navbar.component.html*
```HTML
<div class="navbar">
    <div class="navbar-item">
        <a href="/">Frontpage</a>
    </div>
    <div class="navbar-item">
        <label>
            Subreddit:
            <input (keyup.enter)="toSubreddit()" type="text" [formControl]="subredditInput">
        </label>
        <button (click)="toSubreddit()">Go!</button>
    </div>
</div>
```
We also bind Enter's key up event to *toSubreddit*, so after inputting subreddit name, we can press Enter without clicking the button.

*src/app/components/navbar/navbar.component.scss*
```CSS
.navbar {
    display: flex;
    margin-bottom: 2rem;
    margin-top: 1rem;
}

.navbar .navbar-item {
    margin-right: 1rem;
}
```
We will move some logic in *dashboard* to *navbar*.

*src/app/components/navbar/navbar.component.ts*
```TypeScript
...
import { FormControl } from '@angular/forms';
import { Router } from '@angular/router';
import { CommonService } from '../../services/common.service'
...
export class NavbarComponent implements OnInit {

    subredditInput = new FormControl('');

    constructor(private commonService: CommonService, private router: Router) {
    }

    ngOnInit() {
    }

    toSubreddit(): void {
        this.router.navigate(['/r/' + this.subredditInput.value]);
    }
}
```
Update *dashboard* and *subreddit* view.

*src/app/components/dashboard/dashboard.component.html*
```HTML
<app-navbar></app-navbar>
<app-thread-list [threads]="threads"></app-thread-list>
```
*src/app/components/subreddit/subreddit.component.html*
```HTML
<app-navbar></app-navbar>
<app-thread-list [threads]="threads"></app-thread-list>
```
Run the app to check the result.
```Bash
ng serve
```
![simple-reddit-client-web-by-angular-3-check2.png](angular-reddit-3-check2.png)
### Thread browsing
So we got front page working, subreddit is also working, next we will implement thread browsing.
```Bash
ng generate component components/thread
```
We add a new *reply* model and update *thread* model.

*src/app/models/reply.ts*
```TypeScript
export class Reply {
    id: string;
    content: string;
    author: string;
    score: number;
    permalink: string;
    createdTime: Date;
    replies: Reply[];

    constructor(r: any) {
        this.id = r['id'];
        this.author = r['author'];
        this.score = r['score'];
        this.content = r['body']
        this.permalink = r['permalink'];
        this.createdTime = new Date(r['created'] * 1000);

        if (r['replies']) {
            this.replies = r['replies']['data']['children'].map(reply => {
                return new Reply(reply['data']);
            });
        }
    }
}
```
Each reply can have nested replies inside.

*src/app/models/thread.ts*
```TypeScript
import { Reply } from './reply';

export class Thread {
    ...
    content: string;
    replies: Reply[];

    constructor(t: any) {
        ...
        this.content = t['selftext'];
    }
}
```
Route mapping for thread view.

*src/app/app-routing.module.ts*
```TypeScript

import { ThreadComponent } from './components/thread/thread.component'

const routes: Routes = [
    ...
    {
        path: 'r/:subreddit/comments/:id/:permalink', component: ThreadComponent
    }
];
```
Add the url pattern for reddit thread in config file. We will use [template string](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals) to replace placeholders with variable values later.

*src/assets/config.json*
```JSON
{
    "baseUrl": "https://old.reddit.com",
    "threadUrlFormat": "/r/${subreddit}/comments/${id}/"
}
```
Add getter for our new config property.

*src/app/services/app-config.service.ts*
```TypeScript
get threadUrlFormat() {
    if (!this.appConfig) {
        throw Error('Config file not loaded!');
    }
    return this.appConfig.threadUrlFormat;
}
```
In *common* service, we need a new function to fetch all comments in a thread. The json data structure is simple: the first child is the post content, and second child is list of replies.
We also used *eval* to replace placeholders in config string with values.

*src/app/services/common.service.ts*
```TypeScript
...
import { Reply } from '../models/reply'
...
getComments(subreddit: string, id: string): Observable&#x3C;Thread&#x3E; {
    return this.httpClient.get(this.appConfigService.baseUrl + eval('`' + this.appConfigService.threadUrlFormat + '`') + '.json').pipe(
        map(res => {
            let t = new Thread(res[0]['data']['children'][0]['data']);
            t.replies = res[1]['data']['children'].map(reply => {
                return new Reply(reply['data']);
            });
            return t;
        }
        )
    );
}
```
We finished implementation for the service, next is the component.

*src/app/components/thread/thread.component.ts*
```TypeScript
...
import { Thread } from '../../models/thread'
import { CommonService } from '../../services/common.service'
import { ActivatedRoute } from '@angular/router';
...
export class ThreadComponent implements OnInit {

    thread: Thread;
    subreddit: string;
    id: string;

    constructor(private commonService: CommonService, private route: ActivatedRoute) {
        this.subreddit = this.route.snapshot.paramMap.get('subreddit');
        this.id = this.route.snapshot.paramMap.get('id');
    }

    ngOnInit() {
        this.loadThread();
    }

    loadThread(): void {
        this.commonService.getComments(this.subreddit, this.id).subscribe(res => {
            this.thread = res;
        })
    }
}
```
Here we have 3 properties: *thread* to store data for current viewing thread, *subreddit* and *id* are from url. On component init, add a call to *loadThread*, subscribe to it's observable, and assign it's return value to *thread* property.
### Comment view
HTML is a bit complicated. Due to Reddit's nesting comment system, we need to implement a simple tree view

*src/app/components/thread/thread.component.html*
```HTML
<div class="thread" *ngIf="thread">
    <div class="post">
        <div class="title">
            {{ thread.title }}
        </div>
        <div class="info">
            {{ thread.createdTime| date:'fullDate' }} by <span class="user">{{ thread.author }}</span>
        </div>
        <div class="content">
            {{ thread.content }}
        </div>
        <div class="info">
            <span class="points">{{ thread.score }}</span> pts - <span class="comments">{{ thread.num_comments }}</span>
            comments
        </div>
    </div>
    <div class="replies">
        <ng-container *ngTemplateOutlet="treeViewList; context:{$implicit:thread.replies}">
        </ng-container>
        <ng-template #treeViewList let-list>
            <div class="reply" *ngFor="let reply of list;let i=index">
                <span class="user">{{ reply.author }}</span>
                <div class="content">{{ reply.content }}</div>
                <div class="child">
                    <ng-container *ngTemplateOutlet="treeViewList;
                            context:{$implicit: reply.replies}">
                    </ng-container>
                </div>
            </div>
        </ng-template>
    </div>
</div>
```
Let's dissect the HTML code. The post content is simple, we will focus on the comment part.
```HTML
<ng-container *ngTemplateOutlet="treeViewList; context:{$implicit:thread.replies}">
</ng-container>
```
Here we tell Angular to render an element using <a href="https://angular.io/api/common/NgTemplateOutlet">ngTemplateOutlet</a>, passing *thread.replies* as a variable.
```HTML
<ng-template #treeViewList let-list>
    <div class="reply" *ngFor="let reply of list;let i=index">
        <span class="user">{{ reply.author }}</span>
        <div class="content">{{ reply.content }}</div>
        ...
    </div>
</ng-template>
```
Above is template definition, *list* will have default value from *thread.replies* since we used $implicit key. Then we have to loop through each reply with *ngFor*...
```HTML
<div class="child">
    <ng-container *ngTemplateOutlet="treeViewList;
            context:{$implicit: reply.replies}">
    </ng-container>
</div>
```
... and render all reply's children by using the same template.
Then apply some styling.

*src/app/components/thread/thread.component.scss*
```CSS
.thread .post {
    margin-bottom: 1rem;
}

.thread .post .title {
    font-size: 2rem;
    color: #353535;
}

.thread .post .info .user {
    color: #3d963b;
}

.thread .post .points {
    color: #E64569;
}

.thread .post .comments {
    color: #439ECF;
}

.thread .replies .reply {
    margin-top: 10px;
}

.thread .replies .reply .content {
    padding-bottom: 10px;
    border-bottom: solid 1px lightgray;
}

.thread .replies .reply .child {
    margin-left: 1rem;
}

.thread .replies .reply .user {
    color: #3d963b;
}
```

Run the app to check the result.
```Bash
ng serve
```
![simple-reddit-client-web-by-angular-3-check-3.png](angular-reddit-3-check-3.png)

You can see that the comment content is in markdown format, so we are unable to display it correctly. Luckily, reddit json data also has body_html, which is the HTML version of the comment. We will need to update both *reply* model and thread view.

*src/app/models/reply.ts*
```TypeScript
export class Reply {
    ...

    constructor(r: any) {
        ...
        this.content = r['body_html']
        ...
    }
}
```
*src/app/components/thread/thread.component.html*
```HTML
<div class="content" [innerHTML]="reply.content"></div>
```
We use *innerHTML* property for HTML binding. Now let's check the page again.
![simple-reddit-client-web-by-angular-3-check-4.png](angular-reddit-3-check-4.png)
Ok so we displayed the HTML, but it's being rendered as a string, we need to parse it into HTML.

*src/app/components/thread/thread.component.ts*
```TypeScript
export class ThreadComponent implements OnInit {

    ...
    toHTML(input): any {
        return new DOMParser().parseFromString(input, "text/html").documentElement.textContent;
    }
}
```
*src/app/components/thread/thread.component.html*
```HTML
<div class="content" [innerHTML]="toHTML(reply.content)"></div>
```
Final result.
![simple-reddit-client-web-by-angular-3-check-5.png](angular-reddit-3-check-5.png)
[Source code on github.](https://github.com/tranchikhang/a-reddit)