[![FIWARE Banner](https://fiware.github.io/tutorials.PEP-Proxy/img/fiware.png)](https://www.fiware.org/developers)

[![FIWARE Security](https://nexus.lab.fiware.org/repository/raw/public/badges/chapters/security.svg)](https://github.com/FIWARE/catalogue/blob/master/security/README.md)
[![License: MIT](https://img.shields.io/github/license/fiware/tutorials.PEP-Proxy.svg)](https://opensource.org/licenses/MIT)
[![Support badge](https://img.shields.io/badge/tag-fiware-orange.svg?logo=stackoverflow)](https://stackoverflow.com/questions/tagged/fiware)
<br/>
[![Documentation](https://img.shields.io/readthedocs/fiware-tutorials.svg)](https://fiware-tutorials.rtfd.io)

<!-- prettier-ignore -->

このチュートリアルでは、FIWARE [Wilma](https://fiware-pep-proxy.rtfd.io/) PEP
Proxy と **Keyrock** を組み合わせて、FIWARE Generic Enablers によって公開される
エンドポイントへのアクセスを保護します。ユーザ、または他のアクターは、ログインし
、トークンを使用してサービスにアクセスする必要があります
。[以前のチュートリアル](https://github.com/FIWARE/tutorials.Securing-Access)で
作成したアプリケーション・コードを展開して、分散システム全体のユーザを認証します
。FIWARE Wilma (PEP Proxy) の設計について説明し、他のサービスの認証に関連する
Keyrock GUI と REST API の部分について詳しく説明します。

[cUrl](https://ec.haxx.se/) コマンドは、Keyrock および Wilma REST API にアクセス
するために全面的に使用されています。これらの呼び出しに
[Postman documentation](https://fiware.github.io/tutorials.PEP-Proxy/) も利用で
きます。

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/6b143a6b3ad8bcba69cf)

# コンテンツ

<details>
<summary>詳細 <b>(クリックして拡大)</b></summary>

-   [PEP Proxy を使用したマイクロ・サービスの保護](#securing-microservices-with-a-pep-proxy)
    -   [ID 管理の標準概念](#standard-concepts-of-identity-management)
    -   [:arrow_forward: ビデオ : Wilma PEP Proxy の紹介](#arrow_forward-video--introduction-to-wilma-pep-proxy)
-   [前提条件](#prerequisites)
    -   [Docker](#docker)
    -   [Cygwin](#cygwin)
-   [アーキテクチャ](#architecture)
-   [起動](#start-up)
    -   [登場人物 (Dramatis Personae)](#dramatis-personae)
    -   [REST API を使用した Keyrock へのログイン](#logging-in-to-keyrock-using-the-rest-api)
        -   [パスワードでトークンを作成](#create-token-with-password)
        -   [トークン情報を取得](#get-token-info)
-   [PEP Proxies と IoT Agents の管理](#managing-pep-proxies-and-iot-agents)
    -   [:arrow_forward: ビデオ : Wilma PEP Proxy の設定](#arrow_forward-video--wilma-pep-proxy-configuration)
    -   [PEP Proxies と IoT Agents の管理 - 起動](#managing-pep-proxies-and-iot-agents---start-up)
    -   [PEP Proxy CRUD アクション](#pep-proxy-crud-actions)
        -   [PEP Proxy の作成](#create-a-pep-proxy)
        -   [PEP Proxy の詳細を読み込む](#read-pep-proxy-details)
        -   [PEP Proxy のパスワードをリセット](#reset-password-of-a-pep-proxy)
        -   [PEP Proxy の削除](#delete-a-pep-proxy)
    -   [IoT Agent の CRUD アクション](#iot-agent-crud-actions)
        -   [IoT Agent を作成](#create-an-iot-agent)
        -   [IoT Agent の詳細を読み込む](#read-iot-agent-details)
        -   [IoT Agents の 一覧](#list-iot-agents)
        -   [IoT Agent のパスワードをリセット](#reset-password-of-an-iot-agent)
        -   [IoT Agent を削除](#delete-an-iot-agent)
-   [Orion Context Broker のセキュリティ保護](#securing-the-orion-context-broker)
    -   [Orion の保護 - PEP Proxy の設定](#securing-orion---pep-proxy-configuration)
    -   [Orion の保護 - アプリケーションの設定](#securing-orion---application-configuration)
    -   [Orion の保護 - 起動](#securing-orion---start-up)
        -   [:arrow_forward: ビデオ : REST API を保護](#arrow_forward-video--securing-a-rest-api)
    -   [ユーザが REST API を使用してアプリケーションへのログイン](#user-logs-in-to-the-application-using-the-rest-api)
        -   [PEP Proxy - アクセス・トークンのない Orion へのアクセス拒否](#pep-proxy---no-access-to-orion-without-an-access-token)
        -   [Keyrock - ユーザによるアクセス・トークンの取得](#keyrock---user-obtains-an-access-token)
        -   [PEP Proxy - アクセス・トークンを使用して Orion にアクセス](#pep-proxy---accessing-orion-with-an-access-token)
        -   [PEP Proxy - Authorization: Bearer による Orion へのアクセス](#pep-proxy---accessing-orion-with-an-authorization-bearer)
    -   [Orion の保護 - サンプル・コード](#securing-orion---sample-code)
-   [IoT Agent サウス・ポート の保護](#securing-an-iot-agent-south-port)
    -   [IoT Agent サウス・ポート の保護 - PEP Proxy の設定](#securing-an-iot-agent-south-port---pep-proxy-configuration)
    -   [IoT Agent サウス・ポート の保護 - アプリケーションの設定](#securing-an-iot-agent-south-port---application-configuration)
    -   [サウス・ポート・トラフィックの保護 - 起動](#securing-south-port-traffic---start-up)
    -   [IoT センサが REST API を使用してアプリケーションにログイン](#iot-sensor-logs-in-to-the-application-using-the-rest-api)
        -   [Keyrock - IoT センサによるアクセス・トークンの取得](#keyrock---iot-sensor-obtains-an-access-token)
        -   [PEP Proxy - アクセス・トークンを使用して IoT Agent にアクセス](#pep-proxy---accessing-iot-agent-with-an-access-token)
    -   [サウス・ポート・トラフィックの保護 - サンプル・コード](#securing-south-port-traffic---sample-code)
-   [IoT Agent ノース・ポートの保護](#securing-an-iot-agent-north-port)
    -   [IoT Agent ノース・ポートの保護 - IoT Agent の設定](#securing-an-iot-agent-north-port---iot-agent-configuration)
    -   [IoT Agent ノース・ポートの保護 - 起動](#securing-an-iot-agent-north-port---start-up)
        -   [Keyrock - 永久トークンの取得](#keyrock---obtaining-a-permanent-token)
        -   [IoT Agent - 信頼できるサービス・グループのプロビジョニング](#iot-agent---provisioning-a-trusted-service-group)
        -   [IoT Agent - センサのプロビジョニング](#iot-agent---provisioning-a-sensor)

</details>

<a name="securing-microservices-with-a-pep-proxy"></a>

# PEP Proxy を使用したマイクロ・サービスの保護

> "Oh, it's quite simple. If you are a friend, you speak the password, and the
> doors will open."
>
> — Gandalf (The Fellowship of the Ring by J.R.R Tolkien)

[以前のチュートリアル](https://github.com/FIWARE/tutorials.Securing-Access)は、
アプリケーション内で自身を識別認証されたユーザに基づいて、リソースへのアクセスを
許可または拒否することが可能であることを実証しました。それが `access_token` 見つ
からなかった場合 (レベル 1 - _Authentication Access_, 認証アクセス)、または、与
えられた `access_token` が適切な権利を持っていることを確認すること (レベル 2 -
_Basic Authorization_, 基本認可) は、さまざまラインの実行に続くコードの問題でし
た。FIWARE ベースの Smart Solution 内の他サービスの前に Policy Enforcement Point
(PEP) を置くことで、アクセスを保護する同じ方法を適用できます。

**PEP Proxy** は、保護されたリソースの前方に位置し、"既知の" 公共の場所で見つか
るエンドポイントです。リソース・アクセスのゲート・キーパーとして機能します。ユー
ザ、または他のアクターは、**PEP proxy** を成功させて **PEP proxy** を通過させる
ために、**PEP proxy** に十分な情報を提供する必要があります。**PEP proxy** は、リ
クエストをセキュリティ保護されたリソース自体の実際の場所に渡します。保護されたリ
ソースの実際の場所は外部ユーザには分かりません。**PEP proxy** の背後にあるプライ
ベート・ネットワーク または、別のマシン上にあります。

FIWARE [Wilma](https://fiware-pep-proxy.rtfd.io/) は、FIWARE
[Keyrock](https://fiware-idm.readthedocs.io/en/latest/) Generic Enabler で動作す
るように設計された **PEP proxy** の簡単なインプリケーションです。ユーザが **PEP
proxy** の背後にあるリソースにアクセスしようとするたびに、PEP はユーザの属性を
Policy Decision Point (PDP) に記述し、セキュリティの決定をリクエストし、決定を実
行します。許可または拒否です。許可されたユーザのアクセスが最小限になります。受信
したレスポンスは、セキュリティで保護されたサービスに直接アクセスした場合と同じで
す。権限のないユーザには、**401 - Unauthorized** レスポンスが戻されます。

<a name="standard-concepts-of-identity-management"></a>

## ID 管理の標準概念

**Keyrock** Identity Management データベースには、次の共通オブジェクトがあります
:

-   **User** - 電子メールとパスワードを使用して自分自身を識別できる、登録済みの
    ユーザ。ユーザには、個別にまたはグループとして権利を割り当てることができます
-   **Application** - 一連のマイクロ・サービスで構成された任意のセキュアな
    FIWARE アプリケーション
-   **Organization** - 一連の権利を割り当てることができるユーザのグループ。組織
    の権利を変更すると、その組織のすべてのユーザのアクセスが影響を受けます
-   **OrganizationRole** - ユーザは組織のメンバまたは管理者になることができます
    。管理者は組織にユーザを追加または削除できます。メンバは組織のロールと権限を
    取得するだけです。これにより、各組織はメンバに対して責任を持つことができ、ス
    ーパー管理者 (super-admin) がすべての権限を管理する必要がなくなります
-   **Role** - ロールは、一連のアクセス許可の説明的なバケットです。ロールは、単
    一のユーザまたは組織に割り当てることができます。サインインしたユーザは、自分
    のすべてのロールとその組織に関連付けられているすべてのロールのすべての権限を
    取得します
-   **Permission** - システム内のリソース上で何かを行う能力

さらに、FIWARE アプリケーション内で、2 つの人以外のアプリケーション (non-human
application) のオブジェクトを保護することができます。

-   **IoTAgent** - IoT センサと Context Broker 間のプロキシ
-   **PEPProxy** - ユーザの権利を確認する Generic Enabler 間での使用のためのミド
    ルウェア

オブジェクト間の関係を示します。赤でマークされたエンティティは、このチュートリア
ルで直接使用されています :

![](https://fiware.github.io/tutorials.PEP-Proxy/img/entities.png)

<a name="arrow_forward-video--introduction-to-wilma-pep-proxy"></a>

## :arrow_forward: ビデオ : Wilma PEP Proxy の紹介

[![](https://fiware.github.io/tutorials.Step-by-Step/img/video-logo.png)](https://www.youtube.com/watch?v=8tGbUI18udM "Introduction")

紹介ビデオを見るには上記の画像をクリックしてください :

<a name="prerequisites"></a>

# 前提条件

<a name="docker"></a>

## Docker

物事を単純にするために、両方のコンポーネントが [Docker](https://www.docker.com)
を使用して実行されます。**Docker** は、さまざまコンポーネントをそれぞれの環境に
分離することを可能にするコンテナ・テクノロジです。

-   Docker Windows にインストールするには
    、[こちら](https://docs.docker.com/docker-for-windows/)の手順に従ってくださ
    い
-   Docker Mac にインストールするには
    、[こちら](https://docs.docker.com/docker-for-mac/)の手順に従ってください
-   Docker Linux にインストールするには
    、[こちら](https://docs.docker.com/install/)の手順に従ってください

**Docker Compose** は、マルチコンテナ Docker アプリケーションを定義して実行する
ためのツールです
。[YAML file](https://raw.githubusercontent.com/Fiware/tutorials.Identity-Management/master/docker-compose.yml)
ファイルは、アプリケーションのために必要なサービスを構成するために使用します。つ
まり、すべてのコンテナ・サービスは 1 つのコマンドで呼び出すことができます
。Docker Compose は、デフォルトで Docker for Windows と Docker for Mac の一部と
してインストールされますが、Linux ユーザ
は[ここ](https://docs.docker.com/compose/install/)に記載されている手順に従う必要
があります。

<a name="cygwin"></a>

## Cygwin

シンプルな bash スクリプトを使用してサービスを開始します。Windows ユーザは
[cygwin](http://www.cygwin.com/) をダウンロードして、Windows 上の Linux ディスト
リビューションと同様のコマンドライン機能を提供する必要があります。

<a name="architecture"></a>

# アーキテクチャ

このアプリケーションは、以前のチュートリアルで作成したサービスの周りに **PEP
Proxy** インスタンスを追加することで、既存の在庫管理、および、センサ・ベースのア
プリケーションへのアクセスを保護し、**Keyrock** が使用する **MySQL** データベー
スに事前入力されたデータを使用します
。[Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/),
[IoT Agent for UltraLight 2.0](https://fiware-iotagent-ul.readthedocs.io/en/latest/),
[Keyrock](https://fiware-idm.readthedocs.io/en/latest/) Generic Enabler の 4 つ
の FIWARE コンポーネントを使用し、[Wilma](https://fiware-pep-proxy.rtfd.io/)
**PEP Proxy** の 1 つまたは 2 つのインスタンスを追加して、どのインタフェースを保
護するかを決定します。アプリケーションが _“Powered by FIWARE”_ と認定されるには
、Orion Context Broker を使用するだけで十分です。

Orion Context Broker と IoT Agent はオープンソースの
[MongoDB](https://www.mongodb.com/) 技術を利用して、保持している情報の永続性を保
ちます
。[以前のチュートリアル](https://github.com/FIWARE/tutorials.IoT-Sensors/)で作成
した ダミー IoT デバイスも使用します。**Keyrock** は独自の
[MySQL](https://www.mysql.com/) データベースを使用します。

したがって、全体的なアーキテクチャは次の要素で構成されます :

-   FIWARE
    [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/) は
    、[NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ngsiv2) を使用して
    リクエストを受信します
-   [IoT Agent for UltraLight 2.0](https://fiware-iotagent-ul.readthedocs.io/en/latest/)
    は、[NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ngsiv2) を使用し
    てサウスバウンド・リクエストを受信し、それをデバイスのために
    [UltraLight 2.0](https://fiware-iotagent-ul.readthedocs.io/en/latest/usermanual/index.html#user-programmers-manual)
    に変換します。
-   FIWARE [Keyrock](https://fiware-idm.readthedocs.io/en/latest/) は、以下を含
    んだ、補完的な ID 管理システムを提供します :
    -   アプリケーションとユーザのための OAuth2 認証システム
    -   ID 管理のための Web サイトのグラフィカル・フロントエンド
    -   HTTP リクエストによる ID 管理用の同等の REST API
-   FIWARE [Wilma](https://fiware-pep-proxy.rtfd.io/) は **Orion** および/または
    **IoT Agent** マイクサービスへのアクセスを保護する PEP Proxy
-   [MongoDB](https://www.mongodb.com/) データベース :
    -   **Orion Context Broker** が、データ・エンティティ、サブスクリプション、
        レジストレーションなどのコンテキスト・データ情報を保持するために使用しま
        す
    -   **IoT Agent** が、デバイスの URLs や Keys などのデバイス情報を保持するた
        めに使用します
-   [MySQL](https://www.mysql.com/) データベース :
    -   ユーザ ID、アプリケーション、ロール、および権限を保持するために使用され
        ます
-   **在庫管理フロントエンド**には、次のことを行います :
    -   店舗情報を表示します
    -   各店舗でどの商品を購入できるかを示します
    -   ユーザが製品を"購入"して在庫数を減らすことができます
    -   許可されたユーザを制限されたエリアに入れることができます
-   HTTP を介して実行されている
    [UltraLight 2.0](https://fiware-iotagent-ul.readthedocs.io/en/latest/usermanual/index.html#user-programmers-manual)
    プロトコルを使用す
    る[ダミー IoT デバイス](https://github.com/FIWARE/tutorials.IoT-Sensors/tree/NGSI-v2)のセ
    ットとして機能する Web サーバ。特定のリソースへのアクセスが制限されています
    。

要素間のすべての対話は HTTP リクエストによって開始されるため、エンティティはコン
テナ化され、公開されたポートから実行されます。

チュートリアルの各セクションの具体的なアーキテクチャについては、以下で説明します
。

<a name="start-up"></a>

# 起動

インストールを開始するには、次の手順を実行します :

```console
git clone https://github.com/FIWARE/tutorials.PEP-Proxy.git
cd tutorials.PEP-Proxy
git checkout NGSI-v2

./services create
```

> **注** Docker イメージの最初の作成には最大 3 分かかります

その後、リポジトリ内で提供される
[services](https://github.com/FIWARE/tutorials.PEP-PRoxy/blob/NGSI-v2/services)
Bash スクリプトを実行することによって、コマンドラインからすべてのサービスを初期
化することができます :

```console
./services <command>
```

ここで、<command> は、私たちがアクティベートしたいエクササイズに応じてかわります
。

> :information_source: **注:** クリーンアップをやり直したい場合は、次のコマンド
> を使用して再起動することができます :
>
> ```console
> ./services stop
> ```

<a name="dramatis-personae"></a>

## 登場人物 (Dramatis Personae)

次の `test.com` のメンバは、アプリケーション内に正当なアカウントを持っています。

-   Alice, 彼女は **Keyrock** アプリケーションの管理者になります
-   Bod, スーパー・マーケット・チェーンの地域マネージャ。彼の下に数人のマネージ
    ャがいます :
    -   Manager1
    -   Manager2
-   Charlie, スーパー・マーケット・チェーンのセキュリティ責任者。彼の下に数人の
    警備員がいます。
    -   Detective1
    -   Detective2

次の `example.com` のメンバはアカウントに登録しましたが、アクセスを許可する理由
はありません。

-   Eve - 盗聴者のイブ
-   Mallory - 悪意のある攻撃者のマロリー
-   Rob - 強盗のロブ


<details>
  <summary>
   詳細 <b>(クリックして拡大)</b>
  </summary>

| 名前       | eMail                     | パスワード |
| ---------- | ------------------------- | ---------- |
| alice      | alice-the-admin@test.com  | `test`     |
| bob        | bob-the-manager@test.com  | `test`     |
| charlie    | charlie-security@test.com | `test`     |
| manager1   | manager1@test.com         | `test`     |
| manager2   | manager2@test.com         | `test`     |
| detective1 | detective1@test.com       | `test`     |
| detective2 | detective2@test.com       | `test`     |

| 名前    | eMail               | パスワード |
| ------- | ------------------- | ---------- |
| eve     | eve@example.com     | `test`     |
| mallory | mallory@example.com | `test`     |
| rob     | rob@example.com     | `test`     |

</details>

2 つの組織が Alice によって設定されました :

| 名前       | 説明                                   | UUID                                   |
| ---------- | -------------------------------------- | -------------------------------------- |
| Security   | 店員のためのセキュリティ・グループ     | `security-team-0000-0000-000000000000` |
| Management | ストア・マネージャのための管理グループ | `managers-team-0000-0000-000000000000` |

適切なロールと権限を持つ 1 つのアプリケーションも作成されました :

| キー          | 値                                     |
| ------------- | -------------------------------------- |
| Client ID     | `tutorial-dckr-site-0000-xpresswebapp` |
| Client Secret | `tutorial-dckr-site-0000-clientsecret` |
| URL           | `http://localhost:3000`                |
| RedirectURL   | `http://localhost:3000/login`          |

時間を節約するために
、[以前のチュートリアル](https://github.com/FIWARE/tutorials.Roles-Permissions)か
らユーザと組織を作成するデータがダウンロードされ、起動時に自動的に MySQL データ
ベースに保存されるため、UUIDs が変更されず、データを再入力する必要もありません。

**Keyrock** MySQL データベース は、ユーザ、パスワードなどの格納を含むアプリケー
ションのセキュリティのあらゆる側面を扱います。アクセス権を定義し、OAuth2 認証プ
ロトコルを扱います。完全なデータベース関係図
は[ここ](https://fiware.github.io/tutorials.Securing-Access/img/keyrock-db.png)に
あります。

ユーザや組織、アプリケーションを作成する方法については
、`http://localhost:3005/idm` で、アカウント `alice-the-admin@test.com` とパスワ
ード `test` を使ってログインできます。

![](https://fiware.github.io/tutorials.PEP-Proxy/img/keyrock-log-in.png)

そして、周りを見回してください。

<a name="logging-in-to-keyrock-using-the-rest-api"></a>

## REST API を使用した Keyrock へのログイン

アプリケーションに入るには、ユーザ名とパスワードを入力します。デフォルトの
Super-User は、`alice-the-admin@test.com` と `test` の値を持っています。URL
`https://localhost:3443/v1/auth/tokens` は安全なシステムでも動作するはずです。

<a name="create-token-with-password"></a>

### パスワードでトークンを作成

次の例では、Admin Super-User を使用してログインします :

#### :one: リクエスト:

```console
curl -iX POST \
  'http://localhost:3005/v1/auth/tokens' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "alice-the-admin@test.com",
  "password": "test"
}'
```

#### レスポンス:

レスポンス・ヘッダは、誰がアプリケーションにログオンしているかを識別する
`X-Subject-token` を返します。このトークンは、後続のすべてのリクエストにアクセス
するために必要です。

```
HTTP/1.1 201 Created
X-Subject-Token: d848eb12-889f-433b-9811-6a4fbf0b86ca
Content-Type: application/json; charset=utf-8
Content-Length: 138
ETag: W/"8a-TVwlWNKBsa7cskJw55uE/wZl6L8"
Date: Mon, 30 Jul 2018 12:07:54 GMT
Connection: keep-alive
```

```json
{
    "token": {
        "methods": ["password"],
        "expires_at": "2018-07-30T13:02:37.116Z"
    },
    "idm_authorization_config": {
        "level": "basic",
        "authzforce": false
    }
}
```

<a name="get-token-info"></a>

### トークン情報を取得

ユーザがログインすると、時間制限されたトークンがあれば、ユーザに関する詳細情報を
見つけることができます。

このチュートリアルでは、長続きする
`X-Auth-token=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa` を使用して Alice のふりをす
ることができます。`{{X-Auth-token}}` と `{{X-Subject-token}}` は、Alice が自分自
身について問い合わせを行っている場合に同じ値に設定することができます。

#### :two: リクエスト:

```console
curl -X GET \
  'http://localhost:3005/v1/auth/tokens' \
  -H 'Content-Type: application/json' \
  -H 'X-Auth-token: {{X-Auth-token}}' \
  -H 'X-Subject-token: {{X-Subject-token}}'
```

#### レスポンス:

レスポンスは関連するユーザの詳細を返します :

```json
{
    "access_token": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
    "expires": "2036-07-30T12:04:45.000Z",
    "valid": true,
    "User": {
        "id": "aaaaaaaa-good-0000-0000-000000000000",
        "username": "alice",
        "email": "alice-the-admin@test.com",
        "date_password": "2018-07-30T11:41:14.000Z",
        "enabled": true,
        "admin": true
    }
}
```

<a name="managing-pep-proxies-and-iot-agents"></a>

# PEP Proxies と IoT Agents の管理

[以前のチュートリアル](https://github.com/FIWARE/tutorials.Identity-Management)で
ユーザ・アカウントが作成されました。PEP Proxy などの人以外 (Non-human) のアクタ
ーも同じ方法で設定できます。各 PEP Proxy, IoT Agent または IoT センサのアカウン
トは、Keyrock 内のアプリケーションにリンクされたユーザ名とパスワードで構成されま
す。PEP Proxy アカウントと IoT Agent アカウントは、Keyrock GUI または REST API
を使用して作成できます。

<a name="arrow_forward-video--wilma-pep-proxy-configuration"></a>

## :arrow_forward: ビデオ : Wilma PEP Proxy の設定

[![](https://fiware.github.io/tutorials.Step-by-Step/img/video-logo.png)](https://www.youtube.com/watch?v=b4sYU78skrw "PEP Proxy Configuration")

上の画像をクリックすると、**Keyrock** を使用して、Wilma PEP Proxy を設定する方法
のビデオが表示されます。

<a name="managing-pep-proxies-and-iot-agents---start-up"></a>

## PEP Proxies と IoT Agents の管理 - 起動

システムを起動するには、次のコマンドを実行します :

```console
./services orion
```

これにより、一連のユーザを持つ **Keyrock** を起動します。すでに 2 つの既存のアプ
リケーションと、そのアプリケーションに関連付けられている既存の PEP Proxy アカウ
ントがあります。

<a name="pep-proxy-crud-actions"></a>

## PEP Proxy CRUD アクション

#### GUI

ログインすると、ユーザは自分のアプリケーションに関連付けられた PEP Proxy を作成
して更新することができます。

![](https://fiware.github.io/tutorials.PEP-Proxy/img/create-pep-proxy.png)

#### REST API

あるいは、`/v1/applications/{{application-id}}/pep_proxies` エンドポイント下の適
切な HTTP 動詞 (POST, GET, PATCH および DELETE) に標準 CRUD アクションが割り当て
られます。

<a name="create-a-pep-proxy"></a>

### PEP Proxy の作成

アプリケーション内で新しい PEP Proxy アカウントを作成するには、以前にログインし
た管理者のユーザから、`X-Auth-token` ヘッダ とともに
`/v1/applications/{{application-id}}/pep_proxies` エンドポイントに POST リクエス
トを送信します。

#### :three: リクエスト:

```console
curl -iX POST \
  'http://localhost:3005/v1/applications/{{application-id}}/pep_proxies' \
  -H 'Content-Type: application/json' \
  -H 'X-Auth-token: {{X-Auth-token}}'
```

#### レスポンス:

アプリケーションに関連付けられている既存の PEP Proxy アカウントがない場合は、新
しいアカウントが固有の `id` と `password` を付けて作成され、値がレスポンスに返さ
れます。

```json
{
    "pep_proxy": {
        "id": "pep_proxy_ac80aaf8-0ac3-4bd8-8042-5e8f587679b7",
        "password": "pep_proxy_23d805e7-1b93-434a-8e69-0798dcdd6726"
    }
}
```

<a name="read-pep-proxy-details"></a>

### PEP Proxy の詳細を読み込む

`/v1/applications/{{application-id}}/pep_proxies` エンドポイントに GET リクエス
トを行うと、関連する PEP Proxy アカウントの詳細が返されます。`X-Auth-token` をヘ
ッダに指定してしてください。

#### :four: リクエスト:

```console
curl -X GET \
  'http://localhost:3005/v1/applications/{{application-id}}/pep_proxies/' \
  -H 'X-Auth-token: {{X-Auth-token}}'
```

#### レスポンス:

```json
{
    "pep_proxy": {
        "id": "pep_proxy_f84bcba2-3300-4f13-a4bb-7bdbd358b201",
        "oauth_client_id": "tutorial-dckr-site-0000-xpresswebapp"
    }
}
```

<a name="reset-password-of-a-pep-proxy"></a>

### PEP Proxy のパスワードをリセット

PEP Proxy アカウントのパスワードを更新するには
、`/v1/applications/{{application-id}}/pep_proxies` エンドポイントへの PATCH リ
クエストを実行し、関連する PEP Proxy アカウントの詳細が返されます
。`X-Auth-token` をヘッダに指定してしてください。

#### :five: リクエスト:

```console
curl -X PATCH \
  'http://localhost:3005/v1/applications/{{application-id}}/pep_proxies' \
  -H 'Content-Type: application/json' \
  -H 'X-Auth-token: {{X-Auth-token}}'
```

#### レスポンス:

レスポンスは、PEP Proxy アカウントの新しいパスワードを返します :

```json
{
    "new_password": "pep_proxy_2bc8996e-29bf-4195-ac39-d1116e429602"
}
```

<a name="delete-a-pep-proxy"></a>

### PEP Proxy の削除

既存の PEP Proxy アカウントは、`/v1/applications/{{application-id}}/pep_proxies`
エンドポイントに DELETE リクエストを行うことで削除できます。`X-Auth-token` をヘ
ッダに指定してしてください。

#### :six: リクエスト:

```console
curl -X DELETE \
  'http://localhost:3005/v1/applications/{{application-id}}/pep_proxies' \
  -H 'Content-Type: application/json' \
  -H 'X-Auth-token: {{X-Auth-token}}'
```

<a name="iot-agent-crud-actions"></a>

## IoT Agent の CRUD アクション

#### GUI

PEP Proxy 作成と同様に、サイン・インして、ユーザはアプリケーションに関連付けられ
た IoT センサのアカウントを作成および更新できます。

![](https://fiware.github.io/tutorials.PEP-Proxy/img/create-iot-sensor.png)

#### REST API

あるいは、`/v1/applications/{{application-id}}/iot_agents` エンドポイント下の適
切な HTTP 動詞 (POST, GET, PATCH および DELETE) に標準 CRUD アクションが割り当て
られます。

<a name="create-an-iot-agent"></a>

### IoT Agent を作成

アプリケーション内に新しい IoT Agent アカウントを作成するには、以前にログインし
た管理ユーザから、`X-Auth-token` とともに
`/v1/applications/{{application-id}}/iot_agents` エンドポイントに POST リクエス
トを送信します。

#### :seven: リクエスト:

```console
curl -X POST \
  'http://localhost:3005/v1/applications/{{application-id}}/iot_agents' \
  -H 'Content-Type: application/json' \
  -H 'X-Auth-token: {{X-Auth-token}}'
```

#### レスポンス:

固有の `id` と `password`を持つ新しいアカウントが作成され、値がレスポンスに返さ
れます。

```json
{
    "iot": {
        "id": "iot_sensor_f1d0ca9e-b519-4a8d-b6ae-1246e443dd7e",
        "password": "iot_sensor_8775b438-6e66-4a6e-87c2-45c6525351ee"
    }
}
```

<a name="read-iot-agent-details"></a>

### IoT Agent の詳細を読み込む

GET リクエストを作成すると
、`/v1/applications/{{application-id}}/iot_agents/{{iot-agent-id}}` エンドポイン
トは関連する IoT Agent アカウントの詳細を返します。`X-Auth-token` をヘッダに指定
してしてください。

#### :eight: リクエスト:

```console
curl -X GET \
  'http://localhost:3005/v1/applications/{{application-id}}/iot_agents/{{iot-agent-id}}' \
  -H 'X-Auth-token: {{X-Auth-token}}'
```

#### レスポンス:

```json
{
    "iot": {
        "id": "iot_sensor_00000000-0000-0000-0000-000000000000",
        "oauth_client_id": "tutorial-dckr-site-0000-xpresswebapp"
    }
}
```

<a name="list-iot-agents"></a>

### IoT Agents の 一覧

`/v1/applications/{{application-id}}/iot_agents` エンドポイントに GET リクエスト
を実行することによって、アプリケーションに関連するすべての IoT Agents のリストを
得ることができる。`X-Auth-token` をヘッダに指定してしてください。

#### :nine: リクエスト:

```console
curl -X GET \
  'http://localhost:3005/v1/applications/{{application-id}}/iot_agents' \
  -H 'X-Auth-token: {{X-Auth-token}}'
```

#### レスポンス:

```json
{
    "iots": [
        {
            "id": "iot_sensor_00000000-0000-0000-0000-000000000000"
        },
        {
            "id": "iot_sensor_c0fa0a77-ea9e-4a82-8118-b4d3c6b230b1"
        }
    ]
}
```

<a name="reset-password-of-an-iot-agent"></a>

### IoT Agent のパスワードをリセット

#### :one::zero: リクエスト:

個々の IoT Agent アカウントのパスワードを更新するには
、`/v1/applications/{{application-id}}//iot_agents/{{iot-agent-id}}` エンドポイ
ントに PATCH リクエストを行います。`X-Auth-token` をヘッダに指定してしてください
。

```console
curl -iX PATCH \
  'http://localhost:3005/v1/applications/{{application-id}}/iot_agents/{{iot-agent-id}}' \
  -H 'Content-Type: application/json' \
  -H 'X-Auth-token: {{X-Auth-token}}'
```

#### レスポンス:

レスポンスは、IoT Agent アカウントの新しいパスワードを返します。

```json
{
    "new_password": "iot_sensor_114cb79c-bf69-444a-82a1-e6e85187dacd"
}
```

<a name="delete-an-iot-agent"></a>

### IoT Agent を削除

既存の IoT Agent アカウントは
、`/v1/applications/{{application-id}}/iot_agents/{{iot-agent-id}}` エンドポイン
トに DELETE リクエストを行うことで削除できます。`X-Auth-token` をヘッダに指定し
てしてください。

#### :one::one: リクエスト:

```console
curl -X DELETE \
  'http://localhost:3005/v1/applications/{{application-id}}/iot_agents/{{iot-agent-id}}' \
  -H 'X-Auth-token: {{X-Auth-token}}'
```

<a name="securing-the-orion-context-broker"></a>

# Orion Context Broker の保護

![](https://fiware.github.io/tutorials.PEP-Proxy/img/pep-proxy-orion.png)

<a name="securing-orion---pep-proxy-configuration"></a>

## Orion の保護 - PEP Proxy の設定

`orion-proxy` コンテナは FIWARE **Wilma** のインスタンスであるポート `1027` で待
機し、Orion Context Broker が NGSI リクエストを待機しているデフォルトのポートで
ある、`orion` の ポート `1026` にトラフィックを転送するように設定されます。

```yaml
orion-proxy:
    image: fiware/pep-proxy
    container_name: fiware-orion-proxy
    hostname: orion-proxy
    networks:
        default:
            ipv4_address: 172.18.1.10
    depends_on:
        - keyrock
    ports:
        - "1027:1027"
    expose:
        - "1027"
    environment:
        - PEP_PROXY_APP_HOST=orion
        - PEP_PROXY_APP_PORT=1026
        - PEP_PROXY_PORT=1027
        - PEP_PROXY_IDM_HOST=keyrock
        - PEP_PROXY_HTTPS_ENABLED=false
        - PEP_PROXY_AUTH_ENABLED=false
        - PEP_PROXY_IDM_SSL_ENABLED=false
        - PEP_PROXY_IDM_PORT=3005
        - PEP_PROXY_APP_ID=tutorial-dckr-site-0000-xpresswebapp
        - PEP_PROXY_USERNAME=pep_proxy_00000000-0000-0000-0000-000000000000
        - PEP_PASSWORD=test
        - PEP_PROXY_PDP=idm
        - PEP_PROXY_MAGIC_KEY=1234
```

また、`PEP_PROXY_APP_ID` と `PEP_PROXY_USERNAME` は、通常、**Keyrock** のアプリ
ケーションに新しいエントリを追加して取得しますが、このチュートリアルでは
**MySQL** データベースに起動時のデータを入力することで事前定義されています。

`orion-proxy` コンテナは、単一ポートで待機しています :

-   PEP Proxy ポート `1027` は、純粋にチュートリアルのアクセスのために公開されて
    いるため、cUrl または Postman は同じネットワークの一部ではなくても
    、**Wilma** インスタンスに直接リクエストできます。

| キー                      | 値                                               | 説明                                               |
| ------------------------- | ------------------------------------------------ | -------------------------------------------------- |
| PEP_PROXY_APP_HOST        | `orion`                                          | PEP Proxy の背後にあるサービスのホスト名           |
| PEP_PROXY_APP_PORT        | `1026`                                           | PEP Proxy の背後にあるサービスのポート             |
| PEP_PROXY_PORT            | `1027`                                           | PEP Proxy がリッスンしているポート                 |
| PEP_PROXY_IDM_HOST        | `keyrock`                                        | Keyrock Identity Manager のホスト名                |
| PEP_PROXY_HTTPS_ENABLED   | `false`                                          | PEP Proxy 自体が HTTPS で動作しているかどうか      |
| PEP_PROXY_AUTH_ENABLED    | `false`                                          | PEP Proxy が認可をチェックしているかどうか         |
| PEP_PROXY_IDM_SSL_ENABLED | `false`                                          | Identity Manager が HTTPS で実行されているかどうか |
| PEP_PROXY_IDM_PORT        | `3005`                                           | Identity Manager インスタンスのポート              |
| PEP_PROXY_APP_ID          | `tutorial-dckr-site-0000-xpresswebapp`           |                                                    |
| PEP_PROXY_USERNAME        | `pep_proxy_00000000-0000-0000-0000-000000000000` | PEP Proxy のユーザ名                               |
| PEP_PASSWORD              | `test`                                           | PEP Proxy のパスワード                             |
| PEP_PROXY_PDP             | `idm`                                            | Policy Decision Point を提供するサービスのタイプ   |
| PEP_PROXY_MAGIC_KEY       | `1234`                                           |                                                    |

この例では、PEP Proxy は、レベル 1 - _認証アクセス_ をチェックし、レベル 2 - _基
本認可_ または、レベル 3 - _アドバンスド認可_ をチェックしていません。

<a name="securing-orion---application-configuration"></a>

## Orion の保護 - アプリケーションの設定

チュートリアル・アプリケーションはすでに Keyrock に登録されており、プログラムで
はチュートリアル・アプリケーションは Orion Conext Broker の前にある Wilma PEP
Proxy にリクエストを行います。すべてのリクエストに追加 の `access_token` ヘッダ
が含まれている必要があります。

```yaml
tutorial-app:
    image: fiware/tutorials.context-provider
    hostname: tutorial-app
    container_name: tutorial-app
    depends_on:
        - orion-proxy
        - iot-agent
        - keyrock
    networks:
        default:
            ipv4_address: 172.18.1.7
            aliases:
                - iot-sensors
    expose:
        - "3000"
        - "3001"
    ports:
        - "3000:3000"
        - "3001:3001"
    environment:
        - "WEB_APP_PORT=3000"
        - "SECURE_ENDPOINTS=true"
        - "CONTEXT_BROKER=http://orion-proxy:1027/v2"
        - "KEYROCK_URL=http://localhost"
        - "KEYROCK_IP_ADDRESS=http://172.18.1.5"
        - "KEYROCK_PORT=3005"
        - "KEYROCK_CLIENT_ID=tutorial-dckr-site-0000-xpresswebapp"
        - "KEYROCK_CLIENT_SECRET=tutorial-dckr-site-0000-clientsecret"
        - "CALLBACK_URL=http://localhost:3000/login"
```

すべての `tutorial` コンテナ設定は、以前のチュートリアルで説明されています。ただ
し、以前のすべてのチュートリアルで示されているように、デフォルトのポート
`1026' で **Orion** に直接アクセスするのではなく、すべての Context Broker のトラフィックが`orion-proxy`のポート`1027'
に送信されるように、重要な変更が必要です。ここでは、関連する設定について詳しく説
明します。

| キー                  | 値                                     | 説明                                                                                      |
| --------------------- | -------------------------------------- | ----------------------------------------------------------------------------------------- |
| WEB_APP_PORT          | `3000`                                 | ログイン画面等を表示する web-app が使用するポート                                         |
| KEYROCK_URL           | `http://localhost`                     | ユーザを転送するときのリダイレクトに使用される **Keyrock** Web フロント・エンド自体の URL |
| KEYROCK_IP_ADDRESS    | `http://172.18.1.5`                    | **Keyrock** 通信の URL                                                                    |
| KEYROCK_PORT          | `3005`                                 | **Keyrock** がリッスンしているポート                                                      |
| KEYROCK_CLIENT_ID     | `tutorial-dckr-site-0000-xpresswebapp` | このアプリケーションで **Keyrock** によって定義されたクライアント ID                      |
| KEYROCK_CLIENT_SECRET | `tutorial-dckr-site-0000-clientsecret` | このアプリケーションで **Keyrock** によって定義されたクライアントのシークレット           |
| CALLBACK_URL          | `http://localhost:3000/login`          | チャレンジが成功したときに **Keyrock** が使用するコールバック URL                         |

<a name="securing-orion---start-up"></a>

## Orion の保護 - 起動

**Orion** へのアクセスを保護する PEP Proxy を使用してシステムを起動するには、次
のコマンドを実行します :

```console
./services orion
```

<a name="arrow_forward-video--securing-a-rest-api"></a>

### :arrow_forward: ビデオ : REST API を保護

[![](https://fiware.github.io/tutorials.Step-by-Step/img/video-logo.png)](https://www.youtube.com/watch?v=coxFQEY0_So "Securing a REST API")

上記の画像をクリックすると、Wilma PEP Proxy を使用して REST API を保護するための
ビデオが表示されます

<a name="user-logs-in-to-the-application-using-the-rest-api"></a>

## ユーザが REST API を使用してアプリケーションへのログイン

<a name="pep-proxy---no-access-to-orion-without-an-access-token"></a>

### PEP Proxy - アクセス・トークンのない Orion へのアクセス拒否

セキュアなアクセスは、セキュアなサービスへのすべてのリクエストが PEP Proxy を介
して間接的に行われるようにすることで保証されます。この場合、PEP Proxy は Context
Broker の前にあります。リクエストには、`X-Auth-Token` を含める必要があります。有
効なトークンを提示できないと、アクセスが拒否されます。

#### :one::two: リクエスト:

以下のようにアクセス・トークンなしで PEP Proxy へのリクエストが行われた場合は :

```console
curl -X GET \
  http://localhost:1027/v2/entities/urn:ngsi-ld:Store:001?options=keyValues
```

#### レスポンス

レスポンスは、以下の説明とともに **401 Unauthorized** エラーコードになります :

```
Auth-token not found in request header
```

<a name="keyrock---user-obtains-an-access-token"></a>

### Keyrock - ユーザによるアクセス・トークンの取得

#### :one::three: リクエスト:

ユーザ・クレデンシャルのフローを使用してアプリケーションにログインするには
、`oauth2/token` エンドポイントを使用して、`grant_type=password` とともに
、**Keyrock** に POST リクエストを送信します。例えば、Admin Alice としてログイン
するには :

```console
curl -iX POST \
  'http://localhost:3005/oauth2/token' \
  -H 'Accept: application/json' \
  -H 'Authorization: Basic dHV0b3JpYWwtZGNrci1zaXRlLTAwMDAteHByZXNzd2ViYXBwOnR1dG9yaWFsLWRja3Itc2l0ZS0wMDAwLWNsaWVudHNlY3JldA==' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data "username=alice-the-admin@test.com&password=test&grant_type=password"
```

#### レスポンス

レスポンスは、ユーザを識別するためのアクセス・コードを返します :

```json
{
    "access_token": "a7e22dfe2bd7d883c8621b9eb50797a7f126eeab",
    "token_type": "Bearer",
    "expires_in": 3599,
    "refresh_token": "05e386edd9f95ed0e599c5004db8573e86dff874"
}
```

これは、http:/localhost に、チュートリアル・アプリケーションを入れて、OAuth2 グ
ラントのいずれかを使用してログインすることによっても行うことができます。ログイン
に成功すると、アクセス・トークンが返されます。

<a name="pep-proxy---accessing-orion-with-an-access-token"></a>

### PEP Proxy - アクセス・トークンを使用して Orion にアクセス

示されているように、`X-Auth-Token` ヘッダに有効なアクセス・トークンを含めて PEP
Proxy へのリクエストが行われた場合、そのリクエストは許可され、PEP Proxy の背後に
あるサービス (この場合は Orion Context Broker) が期待通りにデータを返します。

#### :one::four: リクエスト:

```console
curl -X GET \
  http://localhost:1027/v2/entities/urn:ngsi-ld:Store:001?options=keyValues \
  -H 'X-Auth-Token: {{X-Access-token}}'
```

#### レスポンス:

```json
{
    "id": "urn:ngsi-ld:Store:001",
    "type": "Store",
    "address": {
        "streetAddress": "Bornholmer Straße 65",
        "addressRegion": "Berlin",
        "addressLocality": "Prenzlauer Berg",
        "postalCode": "10439"
    },
    "location": {
        "type": "Point",
        "coordinates": [13.3986, 52.5547]
    },
    "name": "Bösebrücke Einkauf"
}
```

<a name="pep-proxy---accessing-orion-with-an-authorization-bearer"></a>

### PEP Proxy - Authorization: Bearer による Orion へのアクセス

標準の `Authorization: Bearer` ヘッダを使用してユーザを識別することもできます。承認されたユーザからのリクエストが許可
され、PEP Proxy の背後にあるサービス (この場合は Orion Context Broker) が期待どおりにデータを返します。

#### :one::five: リクエスト:

```console
curl -X GET \
  http://localhost:1027/v2/entities/urn:ngsi-ld:Store:001?options=keyValues \
  -H 'Authorization: Bearer {{X-Access-token}}'
```

#### レスポンス:

```json
{
    "id": "urn:ngsi-ld:Store:001",
    "type": "Store",
    "address": {
        "streetAddress": "Bornholmer Straße 65",
        "addressRegion": "Berlin",
        "addressLocality": "Prenzlauer Berg",
        "postalCode": "10439"
    },
    "location": {
        "type": "Point",
        "coordinates": [13.3986, 52.5547]
    },
    "name": "Bösebrücke Einkauf"
}
```

<a name="securing-orion---sample-code"></a>

## Orion の保護 - サンプル・コード

ユーザがユーザ・クレデンシャル・グラントを使用してアプリケーションにログインする
と、そのユーザを識別する `access_token` を取得します。`access_token` は、セッシ
ョンに格納されます :

```javascript
function userCredentialGrant(req, res) {
    debug("userCredentialGrant");

    const email = req.body.email;
    const password = req.body.password;

    oa.getOAuthPasswordCredentials(email, password).then(results => {
        req.session.access_token = results.access_token;
        return;
    });
}
```

後続のリクエストごとに、`access_token` は、`X-Auth-Token` ヘッダに設定されます

```javascript
function setAuthHeaders(req) {
    const headers = {};
    if (req.session.access_token) {
        headers["X-Auth-Token"] = req.session.access_token;
    }
    return headers;
}
```

たとえば、アイテムを購入するときに、2 つのリクエストが行われた場合、各リクエスト
に同じ `X-Auth-Token` ヘッダを追加する必要があります。そのため、ユーザを識別して
アクセスを許可することができます。

```javascript
async function buyItem(req, res) {
    const inventory = await retrieveEntity(
        req.params.inventoryId,
        {
            options: "keyValues",
            type: "InventoryItem"
        },
        setAuthHeaders(req)
    );
    const count = inventory.shelfCount - 1;

    await updateExistingEntityAttributes(
        req.params.inventoryId,
        { shelfCount: { type: "Integer", value: count } },
        {
            type: "InventoryItem"
        },
        setAuthHeaders(req)
    );
    res.redirect(`/app/store/${inventory.refStore}/till`);
}
```

<a name="securing-an-iot-agent-south-port"></a>

# IoT Agent サウス・ポート の保護

![](https://fiware.github.io/tutorials.PEP-Proxy/img/pep-proxy-south-port.png)

<a name="securing-an-iot-agent-south-port---pep-proxy-configuration"></a>

## IoT Agent サウス・ポート の保護 - PEP Proxy の設定

`iot-agent-proxy` コンテナは FIWARE **Wilma** のインスタンスである、ポート
`7897` で待機し、`iot-agent` のポート `7896` にトラフィックを転送するように設定
され これは、Ultralight エージェントが、HTTP リクエストのために待機しているデフ
ォルトのポートです。

```yaml
iot-agent-proxy:
    image: fiware/pep-proxy
    container_name: fiware-iot-agent-proxy
    hostname: iot-agent-proxy
    networks:
        default:
            ipv4_address: 172.18.1.11
    depends_on:
        - keyrock
    ports:
        - "7897:7897"
    expose:
        - "7897"
    environment:
        - PEP_PROXY_APP_HOST=iot-agent
        - PEP_PROXY_APP_PORT=7896
        - PEP_PROXY_PORT=7897
        - PEP_PROXY_IDM_HOST=keyrock
        - PEP_PROXY_HTTPS_ENABLED=false
        - PEP_PROXY_AUTH_ENABLED=false
        - PEP_PROXY_IDM_SSL_ENABLED=false
        - PEP_PROXY_IDM_PORT=3005
        - PEP_PROXY_APP_ID=tutorial-dckr-site-0000-xpresswebapp
        - PEP_PROXY_USERNAME=pep_proxy_00000000-0000-0000-0000-000000000000
        - PEP_PASSWORD=test
        - PEP_PROXY_PDP=idm
        - PEP_PROXY_MAGIC_KEY=1234
```

`PEP_PROXY_APP_ID` および `PEP_PROXY_USERNAME` は、通常、**Keyrock** のアプリケ
ーションに新しいエントリを追加することで得られます。ただし、このチュートリアルで
は、**MySQL** データベースに起動時のデータを入力することで事前定義されています。

`iot-agent-proxy` コンテナは、単一ポートで待機しています :

-   PEP Proxy ポート `7897` は、チュートリアル・アクセスのためだけに公開されてい
    るため、cUrl または Postman は、同じネットワークの一部ではなくても、この
    **Wilma** インスタンスに直接リクエストできます。

| キー                      | 値                                               | 説明                                               |
| ------------------------- | ------------------------------------------------ | -------------------------------------------------- |
| PEP_PROXY_APP_HOST        | `iot-agent`                                      | PEP Proxy の背後にあるサービスのホスト名           |
| PEP_PROXY_APP_PORT        | `7896`                                           | PEP Proxy の背後にあるサービスのポート             |
| PEP_PROXY_PORT            | `7897`                                           | PEP Proxy がリッスンしているポート                 |
| PEP_PROXY_IDM_HOST        | `keyrock`                                        | Identity Manager のホスト名                        |
| PEP_PROXY_HTTPS_ENABLED   | `false`                                          | PEP Proxy が HTTPS で動作しているかどうか          |
| PEP_PROXY_AUTH_ENABLED    | `false`                                          | PEP Proxy が認可をチェックしているかどうか         |
| PEP_PROXY_IDM_SSL_ENABLED | `false`                                          | Identity Manager が HTTPS で実行されているかどうか |
| PEP_PROXY_IDM_PORT        | `3005`                                           | Identity Manager インスタンスのポート              |
| PEP_PROXY_APP_ID          | `tutorial-dckr-site-0000-xpresswebapp`           |                                                    |
| PEP_PROXY_USERNAME        | `pep_proxy_00000000-0000-0000-0000-000000000000` | PEP Proxy のユーザ名                               |
| PEP_PASSWORD              | `test`                                           | PEP Proxy のパスワード                             |
| PEP_PROXY_PDP             | `idm`                                            | Policy Decision Point を提供するサービスのタイプ   |
| PEP_PROXY_MAGIC_KEY       | `1234`                                           |                                                    |

この例では、PEP Proxy は、レベル 1 - _認証アクセス_ をチェックし、レベル 2 - _基
本認可_ または、レベル 3 - _アドバンスド認可_ をチェックしていません。

<a name="securing-an-iot-agent-south-port---application-configuration"></a>

## IoT Agent サウス・ポート の保護 - アプリケーションの設定

このチュートリアル・アプリケーションは、ダミー IoT センサのデータを提供する役割
も果たします。IoT センサは、Ultralight 構文でコマンドと測定値を含む HTTP リクエ
ストを出しています。IoT センサのユーザ名とパスワードはすでに **Keyrock** に登録
されていますが、プログラムごとに OAuth2 アクセス・トークンを取得し、**IoT
Agent** の前にある 2 番目の **Wilma** PEP Proxy にリクエストします。


```yaml
tutorial-app:
    image: fiware/tutorials.context-provider
    hostname: tutorial-app
    container_name: tutorial-app
    depends_on:
        - orion-proxy
        - iot-agent-proxy
        - keyrock
    networks:
        default:
            ipv4_address: 172.18.1.7
            aliases:
                - iot-sensors
    expose:
        - "3000"
        - "3001"
    ports:
        - "3000:3000"
        - "3001:3001"
    environment:
        - "IOTA_HTTP_HOST=iot-agent-proxy"
        - "IOTA_HTTP_PORT=7897"
        - "DUMMY_DEVICES_PORT=3001" # Port used by the dummy IoT devices to receive commands
        - "DUMMY_DEVICES_TRANSPORT=HTTP" # Default transport used by dummy IoT devices
        - "DUMMY_DEVICES_API_KEY=4jggokgpepnvsb2uv4s40d59ov"
        - "DUMMY_DEVICES_USER=iot_sensor_00000000-0000-0000-0000-000000000000"
        - "DUMMY_DEVICES_PASSWORD=test"
```

`tutorial` コンテナは、ダミー Ultralight センサをホストします。以前のすべてのチ
ュートリアルに示されているように、**IoT Agent** にポート `7896` で直接アクセスす
るのではなく、すべてのトラフィックが、`iot-agent-proxy` の ポート `7897` に転送
されます。関連する `tutorial` コンテナの設定のほとんどは、以前のチュートリアルで
説明されており、`DUMMY_DEVICES_USER` および `DUMMY_DEVICES_PASSWORD` は新しい追
加項目です。

| キー                    | 値                                                | 説明                                                                                                                              |
| ----------------------- | ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| IOTA_HTTP_HOST          | `iot-agent-proxy`                                 | Ultra Light 2.0 用 IoT Agent を保護する Wilma PEP Proxy のホスト名                                                                |
| IOTA_HTTP_PORT          | `7896`                                            | IoT Agent を保護する Wilma PEP Proxy がリスンしているポート                                                                       |
| DUMMY_DEVICES_PORT      | `3001`                                            | ダミー IoT デバイスがコマンドを受信するために使用するポート                                                                       |
| DUMMY_DEVICES_TRANSPORT | `HTTP`                                            | ダミー IoT デバイスによって使用されるデフォルトのトランスポート                                                                   |
| DUMMY_DEVICES_API_KEY   | `4jggokgpepnvsb2uv4s40d59ov`                      | UltraLight インタラクションに使用されるランダムなセキュリティキー - デバイスと IoT Agent 間のインタラクションの完全性を保証します |
| DUMMY_DEVICES_USER      | `iot_sensor_00000000-0000-0000-0000-000000000000` | **Keyrock** のデバイスに割り当てられたユーザ名                                                                                    |
| DUMMY_DEVICES_PASSWORD  | `test`                                            | **Keyrock** のデバイスに割り当てられたパスワード                                                                                  |

`DUMMY_DEVICES_USER` および `DUMMY_DEVICES_PASSWORD` は、通常、**Keyrock** のア
プリケーションに新しいエントリを追加することで得られますが、このチュートリアルで
は **MySQL** データベースに起動時のデータを入力することで事前定義されています。

<a name="securing-south-port-traffic---start-up"></a>

## サウス・ポート・トラフィックの保護 - 起動

**Orion** と **IoT Agent** の両方へのアクセスを保護する PEP Proxies を使用してシ
ステムを起動するには、次のコマンドを実行します :

```console
./services southport
```

<a name="iot-sensor-logs-in-to-the-application-using-the-rest-api"></a>

## IoT センサが REST API を使用してアプリケーションにログイン

<a name="keyrock---iot-sensor-obtains-an-access-token"></a>

### Keyrock - IoT センサによるアクセス・トークンの取得

IoT センサとしてのログインは、ユーザと同じユーザ・クレデンシャル・フローに従いま
す。ログインしてパスワード `test` でセンサ
`iot_sensor_00000000-0000-0000-0000-000000000000` を特定するには
、`grant_type=password` で `oauth2/token` エンドポイントを使って **Keyrock** に
POST リクエストを送ります :


#### :one::five: リクエスト:

```console
curl -iX POST \
  'http://localhost:3005/oauth2/token' \
  -H 'Accept: application/json' \
  -H 'Authorization: Basic dHV0b3JpYWwtZGNrci1zaXRlLTAwMDAteHByZXNzd2ViYXBwOnR1dG9yaWFsLWRja3Itc2l0ZS0wMDAwLWNsaWVudHNlY3JldA==' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data "username=iot_sensor_00000000-0000-0000-0000-000000000000&password=test&grant_type=password"
```

#### レスポンス

レスポンスは、デバイスを識別するためのアクセス・コードを返します :

```json
{
    "access_token": "a7e22dfe2bd7d883c8621b9eb50797a7f126eeab",
    "token_type": "Bearer",
    "expires_in": 3599,
    "refresh_token": "05e386edd9f95ed0e599c5004db8573e86dff874"
}
```

<a name="pep-proxy---accessing-iot-agent-with-an-access-token"></a>

### PEP Proxy - アクセス・トークンを使用して IoT Agent にアクセス

この例では、デバイス `motion001` からの保護されたリクエストをシミュレートします
。

Ultralight IoT Agent の前にある PEP Proxy への POST リクエストは、事前にプロビジ
ョニングされたリソース `iot/d` エンドポイントを識別し、デバイス `motion001` の測
定値を渡します。`X-Auth-Token` ヘッダを追加すると、リクエスト元が Keyrock に登録
されていると識別され、測定が IoT Agent 自体に正常に渡されます。

#### :one::six: リクエスト:

```console
curl -X POST \
  'http://localhost:7897/iot/d?k=1068318794&i=motion001' \
  -H 'X-Auth-Token: {{X-Access-token}}' \
  -H 'Content-Type: text/plain' \
  -d 'c|1'
```

<a name="securing-south-port-traffic---sample-code"></a>

## サウス・ポート・トラフィックの保護 - サンプル・コード

IoT センサが起動すると、他のユーザと同様にログインしてアクセス・トークンを取得す
る必要があります :

```javascript
const DUMMY_DEVICE_HTTP_HEADERS = { "Content-Type": "text/plain" };
```

```javascript
function initSecureDevices() {
    Security.oa
        .getOAuthPasswordCredentials(process.env.DUMMY_DEVICES_USER, process.env.DUMMY_DEVICES_PASSWORD)
        .then(results => {
            DUMMY_DEVICE_HTTP_HEADERS["X-Auth-Token"] = results.access_token;
            return;
        })
        .catch(error => {
            debug(error);
            return;
        });
}
```

その後、各 HTTP リクエストには、IoT センサを識別するリクエストに `X-Auth-Token`
ヘッダを含みます :

```javascript
const options = {
    method: "POST",
    url: UL_URL,
    qs: { k: UL_API_KEY, i: deviceId },
    headers: DUMMY_DEVICE_HTTP_HEADERS,
    body: state
};

request(options, error => {
    if (error) {
        debug(debugText + " " + error.code);
    }
});
```

<a name="securing-an-iot-agent-north-port"></a>

# IoT Agent ノース・ポートの保護

![](https://fiware.github.io/tutorials.PEP-Proxy/img/pep-proxy-north-port.png)

<a name="securing-an-iot-agent-north-port---iot-agent-configuration"></a>

## IoT Agent ノース・ポートの保護 - IoT Agent の設定

`iot-agent` コンテナはポート `4041` でリッスンしており、ポート `1027` で `orion-proxy` にトラフィックを転送するよう
に設定されています。

```yaml
iot-agent:
    image: fiware/iotagent-ul:${ULTRALIGHT_VERSION}
    hostname: iot-agent
    container_name: fiware-iot-agent
    depends_on:
        - mongo-db
        - orion
    networks:
        - default
    ports:
        - "4041:4041"
        - "7896:7896"
    environment:
        - IOTA_CB_HOST=orion-proxy
        - IOTA_CB_PORT=1027
        - IOTA_NORTH_PORT=4041
        - IOTA_REGISTRY_TYPE=mongodb
        - IOTA_LOG_LEVEL=DEBUG
        - IOTA_TIMESTAMP=true
        - IOTA_CB_NGSI_VERSION=v2
        - IOTA_AUTOCAST=true
        - IOTA_MONGO_HOST=mongo-db
        - IOTA_MONGO_PORT=27017
        - IOTA_MONGO_DB=iotagentul
        - IOTA_HTTP_PORT=7896
        - IOTA_PROVIDER_URL=http://iot-agent:4041
        - IOTA_AUTH_ENABLED=true
        - IOTA_AUTH_TYPE=oauth2
        - IOTA_AUTH_HEADER=Authorization
        - IOTA_AUTH_HOST=keyrock
        - IOTA_AUTH_PORT=3005
        - IOTA_AUTH_URL=http://keyrock:3005
        - IOTA_AUTH_TOKEN_PATH=/oauth2/token
        - IOTA_AUTH_PERMANENT_TOKEN=true
        - IOTA_AUTH_CLIENT_ID=tutorial-dckr-site-0000-xpresswebapp
        - IOTA_AUTH_CLIENT_SECRET=tutorial-dckr-host-0000-clientsecret
```

| キー                      | 値                                     | 説明                                                       |
| ------------------------- | -------------------------------------- | ---------------------------------------------------------- |
| IOTA_AUTH_ENABLED         | `true`                                 | ノース・ポートで認証を使用するかどうか                     |
| IOTA_AUTH_TYPE            | `oauth2`                               | 使用する承認のタイプ (Keyrock は OAuth2 を使用します)      |
| IOTA_AUTH_HEADER          | `Authorization`                        | リクエストに追加されるヘッダの名前                         |
| IOTA_AUTH_HOST            | `keyrock`                              | アプリケーションを保持する Identity Manager                |
| IOTA_AUTH_PORT            | `3005`                                 | Identity Manager がリッスンしているポート                  |
| IOTA_AUTH_URL             | `http://keyrock:3005`                  | 認証要求の URL                                             |
| IOTA_AUTH_CLIENT_ID       | `tutorial-dckr-site-0000-xpresswebapp` | Keyrock 内のアプリケーションの Id                          |
| IOTA_AUTH_CLIENT_SECRET   | `tutorial-dckr-host-0000-clientsecret` | Keyrock 内のアプリケーションのクライアント・シークレット   |
| IOTA_AUTH_PERMANENT_TOKEN | `true`                                 | 永久トークンを使用するかどうか                             |
| IOTA_AUTH_TOKEN_PATH      | `/oauth2/token`                        | トークンを要求するときに使用されるパス                     |

<a name="securing-an-iot-agent-north-port---start-up"></a>

## IoT Agent ノース・ポートの保護 - 起動

**Orion** と **IoT Agent** ノース・ポート間のアクセスを保護する PEP Proxy でシステムを起動するには、次のコマンドを
実行します :


```console
./services northport
```

<a name="keyrock---obtaining-a-permanent-token"></a>

### Keyrock - 永久トークンの取得

Keyrock アプリケーションは、永久トークンを提供するように構成されています。

標準の `Authorization: Basic` ヘッダは、クライアント ID とシークレットの base 64 連結を保持します。パラメータ
`scope=permanent` が追加され、利用可能な場合に永続トークンを取得します。レスポンスには、デバイスのプロビジョニングに
使用できる `access_token` が含まれています。

#### :one::seven: リクエスト:

```console
curl -X POST \
  http://localhost:3005/oauth2/token \
  -H 'Accept: application/json' \
  -H 'Authorization: Basic dHV0b3JpYWwtZGNrci1zaXRlLTAwMDAteHByZXNzd2ViYXBwOnR1dG9yaWFsLWRja3Itc2l0ZS0wMDAwLWNsaWVudHNlY3JldA==' \
  -d 'username=alice-the-admin@test.com&password=test&grant_type=password&scope=permanent'
```

#### レスポンス:

```json
{
    "access_token": "e37aeef5d48c9c1a3d4adf72626a8745918d4355",
    "token_type": "Bearer",
    "scope": ["permanent"]
}
```

<a name="iot-agent---provisioning-a-trusted-service-group"></a>

### IoT Agent - 信頼できるサービス・グループのプロビジョニング

アクセス・トークン (トラスト・トークンとも呼ばれる) をサービス・グループに追加する必要があります。`resource` と `apikey`
は、サービス・グループのプロビジョニング段階で設定された値に対応します。この場合、モーション・センサ・グループは
次のようにプロビジョニングされています:

```json
{
     "apikey":      "1068318794",
     "cbroker":     "http://orion:1026",
     "entity_type": "Motion",
     "resource":    "/iot/d",
}
```

#### :one::eight: リクエスト:

```console
curl -iX PUT \
  'http://localhost:4041/iot/services?resource=/iot/d&apikey=1068318794' \
  -H 'Content-Type: application/json' \
  -H 'fiware-service: openiot' \
  -H 'fiware-servicepath: /' \
  -d '{
     "cbroker": "http://orion-proxy:1027",
     "trust": "30a5ce4c71e416bd199dcdcb7f8bcd8d70e8bb5e"
}'
```

モーション・センサ・リクエストは `orion-proxy` を介して送信され、生成されたトラスト・トークンを使用して自身を識別します。

<a name="iot-agent---provisioning-a-sensor"></a>

### IoT Agent - センサのプロビジョニング

信頼できるサービス・グループが作成されると、通常の方法でデバイスをプロビジョニングできます。

#### :one::nine: リクエスト:

```console
curl -iX POST \
  'http://localhost:4041/iot/devices' \
  -H 'Content-Type: application/json' \
  -H 'fiware-service: openiot' \
  -H 'fiware-servicepath: /' \
  -d '{
 "devices": [
   {
     "device_id":   "motion001",
     "entity_name": "urn:ngsi-ld:Motion:001",
     "entity_type": "Motion",
     "timezone":    "Europe/Berlin",
     "attributes": [
       { "object_id": "c", "name": "count", "type": "Integer" }
     ],
     "static_attributes": [
       { "name":"refStore", "type": "Relationship", "value": "urn:ngsi-ld:Store:001"}
     ]
   }
 ]
}
'
```

---

## License

[MIT](LICENSE) © 2018-2020 FIWARE Foundation e.V.
