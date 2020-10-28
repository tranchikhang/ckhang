---
title: "What are the documents used for system development?"
date: 2020-10-15
summary: "The importance of documentation and common document you may come across"
keywords: "Software engineering, Project management, Documentation, Japanese, Waterfall, IPA"
tags: [Software engineering, Project management, Documentation, Japanese, Waterfall, IPA]
draft: true
---

### The good old waterfall model
If you work in software development, you have probably heard about the waterfall project management methodology (or waterfall model), even if you’ve never used it.
In general, the [waterfall model](https://en.wikipedia.org/wiki/Waterfall_model) is a sequential, linear process of project management that divides software development into pre-defined phases.
![waterfall.png](waterfall.png)
Waterfall is considered a "traditional" and strict approach, proper planning is a must, and there must be a clear picture of what the final product. Everything must be carefully documented and team members will refer to the documentation throughout the process.

### The importance of documentation in system development
In system development process, the time required to create document is not small. But good documentation can provide many benefits:
* Clarify goals and requirements
* Ensure that developers and stakeholders are headed in the same direction
* Keep track of all aspects of the system and improve the quality of the product.
* Assist new user/stakeholder/developer
* Maintenance is easier

### Documents in Software development
In this post, I will present a list of documents you can see in a project using waterfall model and their purposes. There are a few points I want to make:
1. I don't have much experience with other management methodologies like Agile or Scrum, so I will limit it to waterfall model.
2. The documents below are frequently used at Japanese companies (where document management is crucial), so your experience could be different.
3. Different companies have different document management systems/styles, for example, customer may require screen design at requirements phase, or several documents can be merged together.
4. The English names are roughly translated, for example, 業務 does not mean "business" only, but "business operation", "business affairs" in general.

For the sake of completeness, I will also include business related document (mostly appeared in the planning phase), even though developer will rarely see them.

Here is the list

|Phase|Document| |
|:----|:----|:----|
|Business|現状業務の業務フロー図 (AsIs)|Current business flow diagram (AsIs)|
| |システム化後の業務フロー図 (ToBe)|Business flow after systemization diagram (ToBe)|
| |業務機能一覧|List of business functions|
| |システム化業務一覧|List of systemization business|
| |システム化業務説明|Systematization business explanation|
| |業務機能構成表|Business function structure table|
| |ビジネスプロセス関連図|Business process relationship diagram|
| |外部システム関連図|External system relationship diagram|
| |業務処理定義書|Business process definition|
| |システム開発地図|System development map|
|Requirements Definition|要件定義書|Requirements definition|
| |機能一覧|List of Functions|
| |機能定義書|Function definition|
| |画面遷移図|Screen transition diagram|
| |画面一覧|Screen list|
| |画面イメージと項目説明|Screen image and item description|
| |画面アクション明細|Screen action details|
| |帳票一覧|Form list|
| |帳票イメージと項目説明|Form image and item description|
| |バッチ処理一覧|Batch processing list|
| |バッチ機能概要|Batch function overview|
| |バッチジョブフロー|Batch job flow|
| |外部インタフェース一覧|List of external interfaces|
| |外部インタフェース項目定義|External interface item definition|
| |外部インタフェース処理説明|External interface processing explanation|
| |データモデル定義書|Data model definition|
| |データレイアウト概要|Data layout overview|
| |非機能要件の定義|Definition of non-functional requirements|
|Basic Design|基本設計書|Basic design document|
| |システム構成図|System Configuration|
| |ハードウェア構成図|Hardware configuration diagram|
| |ソフトウェア構成図|Software configuration diagram|
| |ネットワーク構成図|Network configuration diagram|
| |設計書記述様式|Design document description style|
| |画面設計書|Screen design|
| |画面レイアウト項目定義|Screen layout item definition|
| |帳票設計書|Form design|
| |帳票レイアウト項目定義|Form layout item definition|
| |帳票編集定義|Form edit definition|
| |オンライン処理設計書|Online processing design|
| |バッチ処理フロー|Batch processing flow|
| |ジョブネット図|Job net diagram|
| |ジョブ設計書|Job design|
| |外部IF設計書|External interface design|
| |メッセージ設計書|Message design|
| |エンティティ一覧|List of entities|
| |エンティティ定義書|Entity definition|
| |ＣＲＵＤ図|CRUD diagram|
| |データ項目定義書|Data item definition|
| |テーブル一覧|Table list|
| |テーブル設計書|Table design|
| |テーブル定義書|Table definition|
| |テーブル関連図（ER図）|Table relationship diagram (ER diagram)|
| |ドメイン一覧／定義|Domain list / definition|
| |コード一覧／定義|Code list / definition|
| |共通処理関数設計|Common processing function design|
|Detail design|詳細設計書|Detailed design document|
| |画面イベント定義|Screen event definition|
| |画面処理詳細定義|Detailed definition of screen processing|
| |クラス図|Class diagram|
| |シーケンス図|Sequence Diagram|
| |ステータス遷移図|State transition diagram|
| |DB更新項目定義|DB update item definition|
| |バッチ処理設計書|Batch processing design|
|Test|単体テスト仕様書兼成績書|Unit test specifications and transcripts|
| |結合テスト仕様書兼成績書|Integration test specifications and transcripts|
| |システムテスト仕様書兼成績書|System test specifications and report|
| |運用テスト仕様書兼成績書|Operation test specifications and report|


References:

[IPA - ドキュメント観点で手戻りを削減](https://www.ipa.go.jp/sec/old/users/seminar/seminar_tokyo_20170615-04.pdf)

[システム開発で作成するドキュメントの体系](https://thinkit.co.jp/article/17064)

[システム開発における成果物とは？要件定義をはじめとした各工程ごとの具体的例](https://www.biz.ne.jp/matome/2005051/)