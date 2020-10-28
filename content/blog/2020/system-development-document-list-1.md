---
title: "Documentation in system development - Business related document"
date: 2020-10-28
summary: "Business related documents in software development"
keywords: "Software engineering, Project management, Documentation, Japanese, IPA"
tags: [Software engineering, Project management, Documentation, Japanese, IPA]
draft: true
---

Continue from my [last post](/blog/2020/system-development-document-list/), this time, I will explain briefly business related document and provide some example pictures.

#### 現状業務の業務フロー図 (AsIs) and システム化後の業務フロー図 (ToBe)
(Current business flow diagram (AsIs) and Business flow after systemization diagram (ToBe))
Sometimes also called 業務フロー定義書.
Describe the current and future business flow, make the work flow visible to the reader.
![b1z-flow-1.jpg](b1z-flow-1.jpg)
![business-flow-2.jpg](business-flow-2.jpg)
![business-asis.png](business-asis.png)
![business-tobe.png](business-tobe.png)

#### 業務機能一覧 (List of business functions) or 業務機能構成表 (Business function structure table)
Describe the structure of organization business, usually from top to bottom, sometimes also include other information like person in charge, how many hours it take per day/month, priority etc.
![business-structure-1.jpg](business-structure-1.jpg)
![business-structure-2.png](business-structure-2.png)

#### システム化業務一覧 (List of systemization business) and システム化業務説明 (Systematization business explanation)
A list of business that will be systematized and explanation.

![systemization-business-1.jpg](systemization-business-1.jpg)
![systemization-business-2.jpg](systemization-business-2.jpg)

#### ビジネスプロセス関連図|Business process relationship diagram
Describe the relationship between each business function, similar to business flow diagram.
![business-process.jpg](business-process.jpg)

#### 外部システム関連図 (External system relationship diagram)
Describe how the system exchange data with other systems.
![external-if.jpg](external-if.jpg)

#### 業務処理定義書 (Business process definition)
Describe detailed business content that cannot be written in the business flow diagram.
![business-process-definition.jpg](business-process-definition.jpg)

#### システム開発地図 (System development map)
A document that organizes the deliverables for each work in the project, which output will be used as input for other task etc.
![dev-map-1.jpg](dev-map-1.jpg)
![dev-map-2.jpg](dev-map-2.jpg)

References:

[業務整理テクニックその１・yFilesを使ったAsIs/ToBeの簡単作成](https://rpa.bigtreetc.com/column/bpmnyfiles/)

[【リスク対策】１．業務フロー図の書き方](https://note.com/iitsuki/n/n8f96057bff7b)

[要件定義工程の成果物一覧](https://pm-rasinban.com/rd-doc)

[【業務可視化関連帳票】業務一覧表とは](https://kashika.biz/analysis-4/)

[IPA - 第1章 システム化業務一覧](https://www.ipa.go.jp/files/000004425.pdf)
[IPA - 第２部合意形成に使う主な図表の解説](https://www.ipa.go.jp/files/000004511.pdf)

[第2回　［システム振舞い編］一覧表に一工夫入れることで漏れや重複をなくす](https://xtech.nikkei.com/it/article/COLUMN/20080611/307596/)

[第4回　［システム振舞い編］発注者が理解しやすいシナリオの記述方法](https://xtech.nikkei.com/it/article/COLUMN/20080707/310297/)

[ユーザのための要件定義ガイド ～要求を明確にするための勘どころ～](https://www.ipa.go.jp/sec/publish/tn16-008.html)

[「システム開発地図」の使い方と作り方 第3回](https://www.itmedia.co.jp/enterprise/articles/1611/22/news156.html)

[プロジェクトを迷走させないシステム開発地図、成果物と担当者が一目でわかる](https://xtech.nikkei.com/it/atcl/column/17/111000511/111600003/)