[![FIWARE Banner](https://fiware.github.io/tutorials.Working-with-Linked-Data/img/fiware.png)](https://www.fiware.org/developers)
[![NGSI LD](https://img.shields.io/badge/NGSI-LD-d6604d.svg)](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.03.01_60/gs_cim009v010301p.pdf)

[![FIWARE Security](https://nexus.lab.fiware.org/repository/raw/public/badges/chapters/security.svg)](https://github.com/FIWARE/catalogue/blob/master/security/README.md)
[![License: MIT](https://img.shields.io/github/license/fiware/tutorials.PEP-Proxy.svg)](https://opensource.org/licenses/MIT)
[![Support badge](https://img.shields.io/badge/tag-fiware-orange.svg?logo=stackoverflow)](https://stackoverflow.com/questions/tagged/fiware)
<br/> [![JSON LD](https://img.shields.io/badge/JSON--LD-1.1-f06f38.svg)](https://w3c.github.io/json-ld-syntax/)
[![Documentation](https://img.shields.io/readthedocs/fiware-tutorials.svg)](https://fiware-tutorials.rtfd.io)

<!-- prettier-ignore -->
このチュートリアルでは、[Apache APISIX](https://apisix.apache.org/) API Gateway を Policy Enforcement Point (PEP) とし
、**Keycloak** と組み合わせて、FIWARE Generic Enablers によって公開されるエンドポイントへのアクセスを保護します。
ユーザ、または他のアクターは、ログインし、有効な JWT トークンを使用してサービスにアクセスする必要があります。
[以前のチュートリアル](https://github.com/FIWARE/tutorials.Securing-Access)で作成したアプリケーション・コードを
展開して、API ゲートウェイ・レベルでロールベースのアクセス制御 (RBAC) を強制します。APISIX のルート設定と Keycloak 
のレルム設定について詳しく説明します。

[cUrl](https://ec.haxx.se/) コマンドは、Keycloak および APISIX REST API にアクセスするために全面的に使用されています。これ
らの呼び出しに [Postman documentation](https://fiware.github.io/tutorials.PEP-Proxy/) も利用できます。

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/6b143a6b3ad8bcba69cf)

# コンテンツ

<details>
<summary>詳細 <b>(クリックして拡大)</b></summary>

-   [PEP Proxy を使用したマイクロ・サービスの保護](#securing-microservices-with-a-pep-proxy)
    -   [ID 管理の標準概念](#standard-concepts-of-identity-management)
    -   [:arrow_forward: ビデオ : APISIX PEP Proxy の紹介](#arrow_forward-video--introduction-to-wilma-pep-proxy)
-   [前提条件](#prerequisites)
    -   [Docker](#docker)
    -   [Cygwin](#cygwin)
-   [アーキテクチャ](#architecture)
-   [起動](#start-up)
    -   [登場人物 (Dramatis Personae)](#dramatis-personae)
    -   [REST API を使用した Keycloak へのログイン](#logging-in-to-keyrock-using-the-rest-api)
        -   [パスワードでトークンを作成](#create-token-with-password)
        -   [トークン情報を取得](#get-token-info)
-   [PEP Proxies と IoT Agents の管理](#configuring-the-apisix-gateway)
    -   [:arrow_forward: ビデオ : APISIX PEP Proxy の設定](#arrow_forward-video--wilma-pep-proxy-configuration)
    -   [PEP Proxies と IoT Agents の管理 - 起動](#configuring-the-apisix-gateway---start-up)
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
-   [Orion-LD Context Broker のセキュリティ保護](#securing-the-orion-context-broker)
    -   [Orion-LD の保護 - PEP Proxy の設定](#securing-orion---pep-proxy-configuration)
    -   [Orion-LD の保護 - アプリケーションの設定](#securing-orion---application-configuration)
    -   [Orion-LD の保護 - 起動](#securing-orion---start-up)
        -   [:arrow_forward: ビデオ : REST API を保護](#arrow_forward-video--securing-a-rest-api)
    -   [ユーザが REST API を使用してアプリケーションへのログイン](#user-logs-in-to-the-application-using-the-rest-api)
        -   [PEP Proxy - アクセス・トークンのない Orion-LD へのアクセス拒否](#pep-proxy---no-access-to-orion-without-an-access-token)
        -   [Keycloak - ユーザによるアクセス・トークンの取得](#keyrock---user-obtains-an-access-token)
        -   [PEP Proxy - アクセス・トークンを使用して Orion-LD にアクセス](#pep-proxy---accessing-orion-with-an-access-token)
        -   [PEP Proxy - Authorization: Bearer による Orion-LD へのアクセス](#pep-proxy---accessing-orion-ld-with-an-authorization-bearer)
    -   [Orion-LD の保護 - サンプル・コード](#securing-orion---sample-code)
-   [IoT Agent サウス・ポート の保護](#securing-an-iot-agent-south-port)
    -   [IoT Agent サウス・ポート の保護 - PEP Proxy の設定](#securing-an-iot-agent-south-port---pep-proxy-configuration)
    -   [IoT Agent サウス・ポート の保護 - アプリケーションの設定](#securing-an-iot-agent-south-port---application-configuration)
    -   [サウス・ポート・トラフィックの保護 - 起動](#securing-south-port-traffic---start-up)
    -   [IoT センサが REST API を使用してアプリケーションにログイン](#iot-sensor-logs-in-to-the-application-using-the-rest-api)
        -   [Keycloak - IoT センサによるアクセス・トークンの取得](#keyrock---iot-sensor-obtains-an-access-token)
        -   [PEP Proxy - アクセス・トークンを使用して IoT Agent にアクセス](#pep-proxy---accessing-iot-agent-with-an-access-token)
    -   [サウス・ポート・トラフィックの保護 - サンプル・コード](#securing-south-port-traffic---sample-code)
-   [IoT Agent ノース・ポートの保護](#securing-an-iot-agent-north-port)
    -   [IoT Agent ノース・ポートの保護 - IoT Agent の設定](#securing-an-iot-agent-north-port---iot-agent-configuration)
    -   [IoT Agent ノース・ポートの保護 - 起動](#securing-an-iot-agent-north-port---start-up)
        -   [Keycloak - 永久トークンの取得](#keyrock---obtaining-a-permanent-token)
        -   [IoT Agent - 信頼できるサービス・グループのプロビジョニング](#iot-agent---provisioning-a-trusted-service-group)
        -   [IoT Agent - センサのプロビジョニング](#iot-agent---provisioning-a-sensor)
</details>

<a name="securing-microservices-with-a-pep-proxy"></a>

# PEP Proxy を使用したマイクロ・サービスの保護

> "Oh, it's quite simple. If you are a friend, you speak the password, and the doors will open."
>
> — Gandalf (The Fellowship of the Ring by J.R.R Tolkien)

[以前のチュートリアル](https://github.com/FIWARE/tutorials.Securing-Access)は、アプリケーション内で自身を識別認証された
ユーザに基づいて、リソースへのアクセスを許可または拒否することが可能であることを実証しました。それが `access_token` 見つ
からなかった場合 (レベル 1 - _Authentication Access_, 認証アクセス)、または、与えられた `access_token` が適切な権利を持
っていることを確認すること (レベル 2 - _Basic Authorization_, 基本認可) は、さまざまラインの実行に続くコードの問題でした
。FIWARE ベースの Smart Solution 内の他サービスの前に Policy Enforcement Point (PEP) を置くことで、アクセスを保護する同
じ方法を適用できます。

**PEP Proxy** は、保護されたリソースの前方に位置し、"既知の" 公共の場所で見つかるエンドポイントです。リソース・アクセス
のゲート・キーパーとして機能します。ユーザ、または他のアクターは、**PEP proxy** を成功させて **PEP proxy** を通過させる
ために、**PEP proxy** に十分な情報を提供する必要があります。**PEP proxy** は、リクエストをセキュリティ保護されたリソース
自体の実際の場所に渡します。保護されたリソースの実際の場所は外部ユーザには分かりません。**PEP proxy** の背後にあるプライ
ベート・ネットワーク または、別のマシン上にあります。

FIWARE [APISIX](https://fiware-pep-proxy.rtfd.io/) は、FIWARE [Keycloak](https://fiware-idm.readthedocs.io/en/latest/)
Generic Enabler で動作するように設計された **PEP proxy** の簡単なインプリケーションです。ユーザが **PEP proxy** の背後に
あるリソースにアクセスしようとするたびに、PEP はユーザの属性を Policy Decision Point (PDP) に記述し、セキュリティの決定
をリクエストし、決定を実行します。許可または拒否です。許可されたユーザのアクセスが最小限になります。受信したレスポンスは
、セキュリティで保護されたサービスに直接アクセスした場合と同じです。権限のないユーザには、**401 - Unauthorized** レスポ
ンスが戻されます。

<a name="standard-concepts-of-identity-management"></a>

## ID 管理の標準概念

**Keycloak** Identity Management データベースには、次の共通オブジェクトがあります :

-   **User** - 電子メールとパスワードを使用して自分自身を識別できる、登録済みのユーザ。ユーザには、個別にまたはグループ
    として権利を割り当てることができます
-   **Application** - 一連のマイクロ・サービスで構成された任意のセキュアな FIWARE アプリケーション
-   **Organization** - 一連の権利を割り当てることができるユーザのグループ。組織の権利を変更すると、その組織のすべてのユ
    ーザのアクセスが影響を受けます
-   **OrganizationRole** - ユーザは組織のメンバまたは管理者になることができます。管理者は組織にユーザを追加または削除で
    きます。メンバは組織のロールと権限を取得するだけです。これにより、各組織はメンバに対して責任を持つことができ、スーパ
    ー管理者 (super-admin) がすべての権限を管理する必要がなくなります
-   **Role** - ロールは、一連のアクセス許可の説明的なバケットです。ロールは、単一のユーザまたは組織に割り当てることがで
    きます。サインインしたユーザは、自分のすべてのロールとその組織に関連付けられているすべてのロールのすべての権限を取得
    します
-   **Permission** - システム内のリソース上で何かを行う能力

さらに、FIWARE アプリケーション内で、2 つの人以外のアプリケーション (non-human application) のオブジェクトを保護すること
ができます。

-   **IoTAgent** - IoT センサと Context Broker 間のプロキシ
-   **PEPProxy** - ユーザの権利を確認する Generic Enabler 間での使用のためのミドルウェア

オブジェクト間の関係を示します。赤でマークされたエンティティは、このチュートリアルで直接使用されています :

![](https://fiware.github.io/tutorials.PEP-Proxy/img/entities.png)

<a name="arrow_forward-video--introduction-to-wilma-pep-proxy"></a>

## :arrow_forward: ビデオ : APISIX PEP Proxy の紹介

[![](https://fiware.github.io/tutorials.Step-by-Step/img/video-logo.png)](https://www.youtube.com/watch?v=8tGbUI18udM "Introduction")

紹介ビデオを見るには上記の画像をクリックしてください :

<a name="prerequisites"></a>

# 前提条件

<a name="docker"></a>

## Docker

物事を単純にするために、両方のコンポーネントが [Docker](https://www.docker.com) を使用して実行されます。**Docker** は、
さまざまコンポーネントをそれぞれの環境に分離することを可能にするコンテナ・テクノロジです。

-   Docker Windows にインストールするには、[こちら](https://docs.docker.com/docker-for-windows/)の手順に従ってください
-   Docker Mac にインストールするには、[こちら](https://docs.docker.com/docker-for-mac/)の手順に従ってください
-   Docker Linux にインストールするには、[こちら](https://docs.docker.com/install/)の手順に従ってください

**Docker Compose** は、マルチコンテナ Docker アプリケーションを定義して実行するためのツールです
。[YAML file](https://raw.githubusercontent.com/Fiware/tutorials.Identity-Management/master/docker-compose.yml) ファイル
は、アプリケーションのために必要なサービスを構成するために使用します。つまり、すべてのコンテナ・サービスは 1 つのコマン
ドで呼び出すことができます。Docker Compose は、デフォルトで Docker for Windows と Docker for Mac の一部としてインストー
ルされますが、Linux ユーザは[ここ](https://docs.docker.com/compose/install/)に記載されている手順に従う必要があります。

<a name="cygwin"></a>

## Cygwin

シンプルな bash スクリプトを使用してサービスを開始します。Windows ユーザは [cygwin](http://www.cygwin.com/) をダウンロー
ドして、Windows 上の Linux ディストリビューションと同様のコマンドライン機能を提供する必要があります。

<a name="architecture"></a>

# アーキテクチャ

このアプリケーションは、以前のチュートリアルで作成したサービスの周りに **PEP Proxy** インスタンスを追加することで、既存
の在庫管理、および、センサ・ベースのアプリケーションへのアクセスを保護し、**Keycloak** が使用する **PostgreSQL** データベース
に事前入力されたデータを使用します。[Orion-LD Context Broker](https://fiware-orion.readthedocs.io/en/latest/),
[IoT Agent for UltraLight 2.0](https://fiware-iotagent-ul.readthedocs.io/en/latest/),
[Keycloak](https://fiware-idm.readthedocs.io/en/latest/) Generic Enabler の 4 つの FIWARE コンポーネントを使用し
、[APISIX](https://fiware-pep-proxy.rtfd.io/) **PEP Proxy** の 1 つまたは 2 つのインスタンスを追加して、どのインタフェー
スを保護するかを決定します。アプリケーションが _“Powered by FIWARE”_ と認定されるには、Orion-LD Context Broker を使用す
るだけで十分です。

Orion-LD Context Broker と IoT Agent はオープンソースの [MongoDB](https://www.mongodb.com/) 技術を利用して、保持している
情報の永続性を保ちます。[以前のチュートリアル](https://github.com/FIWARE/tutorials.IoT-Sensors/)で作成した ダミー IoT デ
バイスも使用します。**Keycloak** は独自の [PostgreSQL](https://www.mysql.com/) データベースを使用します。

したがって、全体的なアーキテクチャは次の要素で構成されます :

-   FIWARE [Orion-LD Context Broker](https://fiware-orion.readthedocs.io/en/latest/) は
    、[NGSI-LD](https://forge.etsi.org/swagger/ui/?url=https://forge.etsi.org/gitlab/NGSI-LD/NGSI-LD/raw/master/spec/updated/full_api.json)
    を使用してリクエストを受信します
-   [IoT Agent for UltraLight 2.0](https://fiware-iotagent-ul.readthedocs.io/en/latest/) は
    、[NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ngsiv2) を使用してサウスバウンド・リクエストを受信し、そ
    れをデバイスのために
    [UltraLight 2.0](https://fiware-iotagent-ul.readthedocs.io/en/latest/usermanual/index.html#user-programmers-manual)
    に変換します。
-   FIWARE [Keycloak](https://fiware-idm.readthedocs.io/en/latest/) は、以下を含んだ、補完的な ID 管理システムを提供しま
    す :
    -   アプリケーションとユーザのための OAuth2 認証システム
    -   ID 管理のための Web サイトのグラフィカル・フロントエンド
    -   HTTP リクエストによる ID 管理用の同等の REST API
-   FIWARE [APISIX](https://fiware-pep-proxy.rtfd.io/) は **Orion-LD** および/または **IoT Agent** マイクサービスへのアク
    セスを保護する PEP Proxy
-   [MongoDB](https://www.mongodb.com/) データベース :
    -   **Orion-LD Context Broker** が、データ・エンティティ、サブスクリプション、レジストレーションなどのコンテキスト・
        データ情報を保持するために使用します
    -   **IoT Agent** が、デバイスの URLs や Keys などのデバイス情報を保持するために使用します
-   [PostgreSQL](https://www.mysql.com/) データベース :
    -   ユーザ ID、アプリケーション、ロール、および権限を保持するために使用されます
-   **在庫管理フロントエンド**には、次のことを行います :
    -   店舗情報を表示します
    -   各店舗でどの商品を購入できるかを示します
    -   ユーザが製品を"購入"して在庫数を減らすことができます
    -   許可されたユーザを制限されたエリアに入れることができます
-   HTTP を介して実行されている
    [UltraLight 2.0](https://fiware-iotagent-ul.readthedocs.io/en/latest/usermanual/index.html#user-programmers-manual)
    プロトコルを使用する[ダミー IoT デバイス](https://github.com/FIWARE/tutorials.IoT-Sensors/tree/NGSI-v2)のセットとし
    て機能する Web サーバ。特定のリソースへのアクセスが制限されています。

要素間のすべての対話は HTTP リクエストによって開始されるため、エンティティはコンテナ化され、公開されたポートから実行され
ます。

チュートリアルの各セクションの具体的なアーキテクチャについては、以下で説明します。

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

その後、リポジトリ内で提供される [services](https://github.com/FIWARE/tutorials.PEP-PRoxy/blob/NGSI-v2/services) Bash ス
クリプトを実行することによって、コマンドラインからすべてのサービスを初期化することができます :

```console
./services <command>
```

ここで、<command> は、私たちがアクティベートしたいエクササイズに応じてかわります。

> :information_source: **注:** クリーンアップをやり直したい場合は、次のコマンドを使用して再起動することができます :
>
> ```console
> ./services stop
> ```

<a name="dramatis-personae"></a>

## 登場人物 (Dramatis Personae)

次の `test.com` のメンバは、アプリケーション内に正当なアカウントを持っています。

-   Alice, 彼女は **Keycloak** アプリケーションの管理者になります
-   Bod, スーパー・マーケット・チェーンの地域マネージャ。彼の下に数人のマネージャがいます :
    -   Manager1
    -   Manager2
-   Charlie, スーパー・マーケット・チェーンのセキュリティ責任者。彼の下に数人の警備員がいます。
    -   Detective1
    -   Detective2

次の `example.com` のメンバはアカウントに登録しましたが、アクセスを許可する理由はありません。

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

時間を節約するために、[以前のチュートリアル](https://github.com/FIWARE/tutorials.Roles-Permissions)からユーザと組織を作
成するデータがダウンロードされ、起動時に自動的に PostgreSQL データベースに保存されるため、UUIDs が変更されず、データを再入力
する必要もありません。

**Keycloak** PostgreSQL データベース は、ユーザ、パスワードなどの格納を含むアプリケーションのセキュリティのあらゆる側面を扱い
ます。アクセス権を定義し、OAuth2 認証プロトコルを扱います。完全なデータベース関係図
は[ここ](https://fiware.github.io/tutorials.Securing-Access/img/keyrock-db.png)にあります。

ユーザや組織、アプリケーションを作成する方法については、`http://localhost:3005/idm` で、アカウント
`alice-the-admin@test.com` とパスワード `test` を使ってログインできます。

![](https://fiware.github.io/tutorials.PEP-Proxy/img/keyrock-log-in.png)

そして、周りを見回してください。

<a name="logging-in-to-keyrock-using-the-rest-api"></a>

## REST API を使用した Keycloak へのログイン

アプリケーションに入るには、ユーザ名とパスワードを入力します。デフォルトの Super-User は、`alice-the-admin@test.com` と
`test` の値を持っています。URL `https://localhost:3443/realms/farm-management/protocol/openid-connect/token` は安全なシステムでも動作するはずです。

<a name="create-token-with-password"></a>

### パスワードでトークンを作成

次の例では、Admin Super-User を使用してログインします :

#### :one: リクエスト:

```console
curl -iX POST \
  'http://localhost:3005/realms/farm-management/protocol/openid-connect/token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=alice-the-admin@test.com&password=test&grant_type=password&client_id=ngsi-ld-farm&client_secret=1234'
```

#### レスポンス:

レスポンス・ヘッダは、誰がアプリケーションにログオンしているかを識別する `access_token` を返します。このトークンは、
後続のすべてのリクエストにアクセスするために必要です。

```
HTTP/1.1 201 Created
Content-Security-Policy: default-src 'self' img-src 'self' data:;script-src 'self' 'unsafe-inline';style-src 'self' https: 'unsafe-inline'
X-DNS-Prefetch-Control: off
Expect-CT: max-age=0
X-Frame-Options: SAMEORIGIN
Strict-Transport-Security: max-age=15552000; includeSubDomains
X-Download-Options: noopen
X-Content-Type-Options: nosniff
X-Permitted-Cross-Domain-Policies: none
Referrer-Policy: no-referrer
X-XSS-Protection: 0
Cache-Control: no-cache, private, no-store, must-revalidate, max-stale=0, post-check=0, pre-check=0
access_token: 730ba40f-8787-490e-aea8-9f1d98cc87e6
Content-Type: application/json; charset=utf-8
Content-Length: 138
ETag: W/"8a-hYrW1bqaSy3GVQI34aexyHgPYmg"
Set-Cookie: session=eyJyZWRpciI6Ii8ifQ==; path=/; expires=Thu, 03 Dec 2020 16:46:08 GMT; httponly
Set-Cookie: session.sig=vwpRi_eyA0W2C0YYa-6mzMBHBIk; path=/; expires=Thu, 03 Dec 2020 16:46:08 GMT; httponly
Date: Thu, 03 Dec 2020 15:46:08 GMT
Connection: keep-alive
```

```json
{
    "token": {
        "methods": ["password"],
        "expires_at": "2020-12-03T16:47:28.462Z"
    },
    "idm_authorization_config": {
        "level": "basic",
        "authzforce": false
    }
}
```

<a name="get-token-info"></a>

### トークン情報を取得

ユーザがログインすると、時間制限されたトークンがあれば、ユーザに関する詳細情報を見つけることができます。

このチュートリアルでは、長続きする `Authorization=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa` を使用して Alice のふりをすること
ができます。`{{Authorization}}` と `{{access_token}}` は、Alice が自分自身について問い合わせを行っている場合に同じ値に
設定することができます。

#### :two: リクエスト:

```console
curl -X GET \
  'http://localhost:3005/realms/farm-management/protocol/openid-connect/token' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: {{Authorization}}' \
  -H 'access_token: {{access_token}}'
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

<a name="configuring-the-apisix-gateway"></a>

# PEP Proxies と IoT Agents の管理

[以前のチュートリアル](https://github.com/FIWARE/tutorials.Identity-Management)でユーザ・アカウントが作成されました。PEP
Proxy などの人以外 (Non-human) のアクターも同じ方法で設定できます。各 PEP Proxy, IoT Agent または IoT センサのアカウント
は、Keycloak 内のアプリケーションにリンクされたユーザ名とパスワードで構成されます。PEP Proxy アカウントと IoT Agent アカ
ウントは、Keycloak GUI または REST API を使用して作成できます。

<a name="arrow_forward-video--wilma-pep-proxy-configuration"></a>

## :arrow_forward: ビデオ : APISIX PEP Proxy の設定

[![](https://fiware.github.io/tutorials.Step-by-Step/img/video-logo.png)](https://www.youtube.com/watch?v=b4sYU78skrw "PEP Proxy Configuration")

上の画像をクリックすると、**Keycloak** を使用して、APISIX PEP Proxy を設定する方法のビデオが表示されます。

<a name="configuring-the-apisix-gateway---start-up"></a>

## PEP Proxies と IoT Agents の管理 - 起動

システムを起動するには、次のコマンドを実行します :

```console
./services orion
```

これにより、一連のユーザを持つ **Keycloak** を起動します。すでに 2 つの既存のアプリケーションと、そのアプリケーションに関
連付けられている既存の PEP Proxy アカウントがあります。

<a name="pep-proxy-crud-actions"></a>

## PEP Proxy CRUD アクション

#### GUI

ログインすると、ユーザは自分のアプリケーションに関連付けられた PEP Proxy を作成して更新することができます。

![](https://fiware.github.io/tutorials.PEP-Proxy/img/create-pep-proxy.png)

#### REST API

あるいは、`/v1/applications/{{application-id}}/pep_proxies` エンドポイント下の適切な HTTP 動詞 (POST, GET, PATCH および
DELETE) に標準 CRUD アクションが割り当てられます。

<a name="create-a-pep-proxy"></a>

### PEP Proxy の作成

アプリケーション内で新しい PEP Proxy アカウントを作成するには、以前にログインした管理者のユーザから、`Authorization` ヘッ
ダ とともに `/v1/applications/{{application-id}}/pep_proxies` エンドポイントに POST リクエストを送信します。

#### :three: リクエスト:

```console
curl -iX POST \
  'http://localhost:3005/v1/applications/{{application-id}}/pep_proxies' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: {{Authorization}}'
```

#### レスポンス:

アプリケーションに関連付けられている既存の PEP Proxy アカウントがない場合は、新しいアカウントが固有の `id` と `password`
を付けて作成され、値がレスポンスに返されます。

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

`/v1/applications/{{application-id}}/pep_proxies` エンドポイントに GET リクエストを行うと、関連する PEP Proxy アカウント
の詳細が返されます。`Authorization` をヘッダに指定してしてください。

#### :four: リクエスト:

```console
curl -X GET \
  'http://localhost:3005/v1/applications/{{application-id}}/pep_proxies/' \
  -H 'Authorization: {{Authorization}}'
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

PEP Proxy アカウントのパスワードを更新するには、`/v1/applications/{{application-id}}/pep_proxies` エンドポイントへの
PATCH リクエストを実行し、関連する PEP Proxy アカウントの詳細が返されます。`Authorization` をヘッダに指定してしてください
。

#### :five: リクエスト:

```console
curl -X PATCH \
  'http://localhost:3005/v1/applications/{{application-id}}/pep_proxies' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: {{Authorization}}'
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

既存の PEP Proxy アカウントは、`/v1/applications/{{application-id}}/pep_proxies` エンドポイントに DELETE リクエストを行
うことで削除できます。`Authorization` をヘッダに指定してしてください。

#### :six: リクエスト:

```console
curl -X DELETE \
  'http://localhost:3005/v1/applications/{{application-id}}/pep_proxies' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: {{Authorization}}'
```

<a name="iot-agent-crud-actions"></a>

## IoT Agent の CRUD アクション

#### GUI

PEP Proxy 作成と同様に、サイン・インして、ユーザはアプリケーションに関連付けられた IoT センサのアカウントを作成および更
新できます。

![](https://fiware.github.io/tutorials.PEP-Proxy/img/create-iot-sensor.png)

#### REST API

あるいは、`/v1/applications/{{application-id}}/iot_agents` エンドポイント下の適切な HTTP 動詞 (POST, GET, PATCH および
DELETE) に標準 CRUD アクションが割り当てられます。

<a name="create-an-iot-agent"></a>

### IoT Agent を作成

アプリケーション内に新しい IoT Agent アカウントを作成するには、以前にログインした管理ユーザから、`Authorization` とともに
`/v1/applications/{{application-id}}/iot_agents` エンドポイントに POST リクエストを送信します。

#### :seven: リクエスト:

```console
curl -X POST \
  'http://localhost:3005/v1/applications/{{application-id}}/iot_agents' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: {{Authorization}}'
```

#### レスポンス:

固有の `id` と `password`を持つ新しいアカウントが作成され、値がレスポンスに返されます。

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

GET リクエストを作成すると、`/v1/applications/{{application-id}}/iot_agents/{{iot-agent-id}}` エンドポイントは関連する
IoT Agent アカウントの詳細を返します。`Authorization` をヘッダに指定してしてください。

#### :eight: リクエスト:

```console
curl -X GET \
  'http://localhost:3005/v1/applications/{{application-id}}/iot_agents/{{iot-agent-id}}' \
  -H 'Authorization: {{Authorization}}'
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

`/v1/applications/{{application-id}}/iot_agents` エンドポイントに GET リクエストを実行することによって、アプリケーション
に関連するすべての IoT Agents のリストを得ることができる。`Authorization` をヘッダに指定してしてください。

#### :nine: リクエスト:

```console
curl -X GET \
  'http://localhost:3005/v1/applications/{{application-id}}/iot_agents' \
  -H 'Authorization: {{Authorization}}'
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
、`/v1/applications/{{application-id}}//iot_agents/{{iot-agent-id}}` エンドポイントに PATCH リクエストを行います
。`Authorization` をヘッダに指定してしてください。

```console
curl -iX PATCH \
  'http://localhost:3005/v1/applications/{{application-id}}/iot_agents/{{iot-agent-id}}' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: {{Authorization}}'
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

既存の IoT Agent アカウントは、`/v1/applications/{{application-id}}/iot_agents/{{iot-agent-id}}` エンドポイントに DELETE
リクエストを行うことで削除できます。`Authorization` をヘッダに指定してしてください。

#### :one::one: リクエスト:

```console
curl -X DELETE \
  'http://localhost:3005/v1/applications/{{application-id}}/iot_agents/{{iot-agent-id}}' \
  -H 'Authorization: {{Authorization}}'
```

<a name="securing-the-orion-context-broker"></a>

# Orion-LD Context Broker の保護

![](https://fiware.github.io/tutorials.PEP-Proxy/img/pep-proxy-orion.png)

<a name="securing-orion---pep-proxy-configuration"></a>

## Orion-LD の保護 - PEP Proxy の設定

`orion-proxy` コンテナは FIWARE **APISIX** のインスタンスであるポート `1027` で待機し、Orion-LD Context Broker が NGSI リ
クエストを待機しているデフォルトのポートである、`orion` の ポート `1026` にトラフィックを転送するように設定されます。

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

また、`PEP_PROXY_APP_ID` と `PEP_PROXY_USERNAME` は、通常、**Keycloak** のアプリケーションに新しいエントリを追加して取得
しますが、このチュートリアルでは **PostgreSQL** データベースに起動時のデータを入力することで事前定義されています。

`orion-proxy` コンテナは、単一ポートで待機しています :

-   PEP Proxy ポート `1027` は、純粋にチュートリアルのアクセスのために公開されているため、cUrl または Postman は同じネッ
    トワークの一部ではなくても、**APISIX** インスタンスに直接リクエストできます。

| キー                      | 値                                               | 説明                                               |
| ------------------------- | ------------------------------------------------ | -------------------------------------------------- |
| PEP_PROXY_APP_HOST        | `orion`                                          | PEP Proxy の背後にあるサービスのホスト名           |
| PEP_PROXY_APP_PORT        | `1026`                                           | PEP Proxy の背後にあるサービスのポート             |
| PEP_PROXY_PORT            | `1027`                                           | PEP Proxy がリッスンしているポート                 |
| PEP_PROXY_IDM_HOST        | `keyrock`                                        | Keycloak Identity Manager のホスト名                |
| PEP_PROXY_HTTPS_ENABLED   | `false`                                          | PEP Proxy 自体が HTTPS で動作しているかどうか      |
| PEP_PROXY_AUTH_ENABLED    | `false`                                          | PEP Proxy が認可をチェックしているかどうか         |
| PEP_PROXY_IDM_SSL_ENABLED | `false`                                          | Identity Manager が HTTPS で実行されているかどうか |
| PEP_PROXY_IDM_PORT        | `3005`                                           | Identity Manager インスタンスのポート              |
| PEP_PROXY_APP_ID          | `tutorial-dckr-site-0000-xpresswebapp`           |                                                    |
| PEP_PROXY_USERNAME        | `pep_proxy_00000000-0000-0000-0000-000000000000` | PEP Proxy のユーザ名                               |
| PEP_PASSWORD              | `test`                                           | PEP Proxy のパスワード                             |
| PEP_PROXY_PDP             | `idm`                                            | Policy Decision Point を提供するサービスのタイプ   |
| PEP_PROXY_MAGIC_KEY       | `1234`                                           |                                                    |

この例では、PEP Proxy は、レベル 1 - _認証アクセス_ をチェックし、レベル 2 - _基本認可_ または、レベル 3 - _アドバンスド
認可_ をチェックしていません。

<a name="securing-orion---application-configuration"></a>

## Orion-LD の保護 - アプリケーションの設定

チュートリアル・アプリケーションはすでに Keycloak に登録されており、プログラムではチュートリアル・アプリケーションは
Orion-LD Conext Broker の前にある APISIX PEP Proxy にリクエストを行います。すべてのリクエストに追加 の `access_token` ヘ
ッダが含まれている必要があります。

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

すべての `tutorial` コンテナ設定は、以前のチュートリアルで説明されています。ただし、以前のすべてのチュートリアルで示され
ているように、デフォルトのポート
`1026' で **Orion-LD** に直接アクセスするのではなく、すべての Context Broker のトラフィックが`orion-proxy`のポート`1027'
に送信されるように、重要な変更が必要です。ここでは、関連する設定について詳しく説明します。

| キー                  | 値                                     | 説明                                                                                      |
| --------------------- | -------------------------------------- | ----------------------------------------------------------------------------------------- |
| WEB_APP_PORT          | `3000`                                 | ログイン画面等を表示する web-app が使用するポート                                         |
| KEYROCK_URL           | `http://localhost`                     | ユーザを転送するときのリダイレクトに使用される **Keycloak** Web フロント・エンド自体の URL |
| KEYROCK_IP_ADDRESS    | `http://172.18.1.5`                    | **Keycloak** 通信の URL                                                                    |
| KEYROCK_PORT          | `3005`                                 | **Keycloak** がリッスンしているポート                                                      |
| KEYROCK_CLIENT_ID     | `tutorial-dckr-site-0000-xpresswebapp` | このアプリケーションで **Keycloak** によって定義されたクライアント ID                      |
| KEYROCK_CLIENT_SECRET | `tutorial-dckr-site-0000-clientsecret` | このアプリケーションで **Keycloak** によって定義されたクライアントのシークレット           |
| CALLBACK_URL          | `http://localhost:3000/login`          | チャレンジが成功したときに **Keycloak** が使用するコールバック URL                         |

<a name="securing-orion---start-up"></a>

## Orion-LD の保護 - 起動

**Orion-LD** へのアクセスを保護する PEP Proxy を使用してシステムを起動するには、次のコマンドを実行します :

```console
./services orion
```

<a name="arrow_forward-video--securing-a-rest-api"></a>

### :arrow_forward: ビデオ : REST API を保護

[![](https://fiware.github.io/tutorials.Step-by-Step/img/video-logo.png)](https://www.youtube.com/watch?v=coxFQEY0_So "Securing a REST API")

上記の画像をクリックすると、APISIX PEP Proxy を使用して REST API を保護するためのビデオが表示されます

<a name="user-logs-in-to-the-application-using-the-rest-api"></a>

## ユーザが REST API を使用してアプリケーションへのログイン

<a name="pep-proxy---no-access-to-orion-without-an-access-token"></a>

### PEP Proxy - アクセス・トークンのない Orion-LD へのアクセス拒否

セキュアなアクセスは、セキュアなサービスへのすべてのリクエストが PEP Proxy を介して間接的に行われるようにすることで保証
されます。この場合、PEP Proxy は Context Broker の前にあります。リクエストには、`Authorization` を含める必要があります。
有効なトークンを提示できないと、アクセスが拒否されます。

#### :one::two: リクエスト:

以下のようにアクセス・トークンなしで PEP Proxy へのリクエストが行われた場合は :

```console
curl -X GET 'http://localhost:1030/orion/ngsi-ld/v1/entities/urn:ngsi-ld:Building:farm001?options=keyValues' \
  -H 'Link: <https://fiware.github.io/tutorials.Step-by-Step/tutorials-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"' \
  -H 'Content-Type: application/json'
```

#### レスポンス

レスポンスは、以下の説明とともに **401 Unauthorized** エラーコードになります :

```
Auth-token not found in request header
```

<a name="keyrock---user-obtains-an-access-token"></a>

### Keycloak - ユーザによるアクセス・トークンの取得

#### :one::three: リクエスト:

ユーザ・クレデンシャルのフローを使用してアプリケーションにログインするには、`oauth2/token` エンドポイントを使用して
、`grant_type=password` とともに、**Keycloak** に POST リクエストを送信します。例えば、Admin Alice としてログインするには
:

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
    "scope":["bearer"]
}
```

これは、http:/localhost に、チュートリアル・アプリケーションを入れて、OAuth2 グラントのいずれかを使用してログインするこ
とによっても行うことができます。ログインに成功すると、アクセス・トークンが返されます。

<a name="pep-proxy---accessing-orion-with-an-access-token"></a>

### PEP Proxy - アクセス・トークンを使用して Orion-LD にアクセス

前のレスポンスの `Authorization` キーで取得された値を持つ `Authorization` ヘッダーに有効なアクセス・トークンを含めて PEP
Proxy へのリクエストが行われた場合、リクエストは許可され、PEP Proxy の背後にあるサービス (この場合は Orion-LD Context
Broker) が期待どおりにデータを返します。

#### :one::four: リクエスト:

```console
curl -X GET 'http://localhost:1030/orion/ngsi-ld/v1/entities/urn:ngsi-ld:Building:farm001?options=keyValues' \
  -H 'Link: <https://fiware.github.io/tutorials.Step-by-Step/tutorials-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: {{Authorization}}'
```

#### レスポンス:

レスポンスは、Farm001 に関する情報を返します:

```json
{
    "@context": "https://fiware.github.io/tutorials.Step-by-Step/tutorials-context.jsonld",
    "id": "urn:ngsi-ld:Building:farm001",
    "type": "Building",
    "category": "farm",
    "address": {
        "streetAddress": "Großer Stern 1",
        "addressRegion": "Berlin",
        "addressLocality": "Tiergarten",
        "postalCode": "10557"
    },
    "location": {
        "type": "Point",
        "coordinates": [13.3505, 52.5144]
    },
    "name": "Victory Farm",
    "owner": "urn:ngsi-ld:Person:person001"
}
```

<a name="pep-proxy---accessing-orion-ld-with-an-authorization-bearer"/>

### PEP Proxy - Authorization: Bearer による Orion-LD へのアクセス

標準の `Authorization: Bearer` ヘッダを使用してユーザを識別することもできます。承認されたユーザからのリクエストが許可さ
れ、PEP Proxy の背後にあるサービス (この場合は Orion-LD Context Broker) が期待どおりにデータを返します。

#### :one::five: Request:

```console
curl -X GET 'http://localhost:1030/orion/ngsi-ld/v1/entities/urn:ngsi-ld:Building:barn002?options=keyValues' \
  -H 'Link: <https://fiware.github.io/tutorials.Step-by-Step/tutorials-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {{Authorization}}'
```

#### Response:

```json
{
    "@context": "https://fiware.github.io/tutorials.Step-by-Step/tutorials-context.jsonld",
    "id": "urn:ngsi-ld:Building:barn002",
    "type": "Building",
    "category": "barn",
    "address": {
        "streetAddress": "Straße des 17. Juni",
        "addressRegion": "Berlin",
        "addressLocality": "Tiergarten",
        "postalCode": "10557"
    },
    "location": {
        "type": "Point",
        "coordinates": [13.3698, 52.5163]
    },
    "name": "Big Red Barn",
    "owner": "urn:ngsi-ld:Person:person001"
}
```

<a name="securing-orion---sample-code"></a>

## Orion-LD の保護 - サンプル・コード

ユーザがユーザ・クレデンシャル・グラントを使用してアプリケーションにログインすると、そのユーザを識別する `access_token`
を取得します。`access_token` は、セッションに格納されます :

```javascript
function userCredentialGrant(req, res) {
    debug("userCredentialGrant");

    const email = req.body.email;
    const password = req.body.password;

    oa.getOAuthPasswordCredentials(email, password).then((results) => {
        req.session.access_token = results.access_token;
        return;
    });
}
```

後続のリクエストごとに、`access_token` は、`Authorization` ヘッダに設定されます

```javascript
function setAuthHeaders(req) {
    const headers = {};
    if (req.session.access_token) {
        headers["Authorization"] = req.session.access_token;
    }
    return headers;
}
```

たとえば、アイテムを購入するときに、2 つのリクエストが行われた場合、各リクエストに同じ `Authorization` ヘッダを追加する必
要があります。そのため、ユーザを識別してアクセスを許可することができます。

```javascript
async function buyItem(req, res) {
    const inventory = await retrieveEntity(
        req.params.inventoryId,
        {
            options: "keyValues",
            type: "InventoryItem",
        },
        setAuthHeaders(req)
    );
    const count = inventory.shelfCount - 1;

    await updateExistingEntityAttributes(
        req.params.inventoryId,
        { shelfCount: { type: "Integer", value: count } },
        {
            type: "InventoryItem",
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

`iot-agent-proxy` コンテナは FIWARE **APISIX** のインスタンスである、ポート `7897` で待機し、`iot-agent` のポート `7896`
にトラフィックを転送するように設定され これは、Ultralight エージェントが、HTTP リクエストのために待機しているデフォルト
のポートです。

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

`PEP_PROXY_APP_ID` および `PEP_PROXY_USERNAME` は、通常、**Keycloak** のアプリケーションに新しいエントリを追加することで
得られます。ただし、このチュートリアルでは、**PostgreSQL** データベースに起動時のデータを入力することで事前定義されています。

`iot-agent-proxy` コンテナは、単一ポートで待機しています :

-   PEP Proxy ポート `7897` は、チュートリアル・アクセスのためだけに公開されているため、cUrl または Postman は、同じネッ
    トワークの一部ではなくても、この **APISIX** インスタンスに直接リクエストできます。

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

この例では、PEP Proxy は、レベル 1 - _認証アクセス_ をチェックし、レベル 2 - _基本認可_ または、レベル 3 - _アドバンスド
認可_ をチェックしていません。

<a name="securing-an-iot-agent-south-port---application-configuration"></a>

## IoT Agent サウス・ポート の保護 - アプリケーションの設定

このチュートリアル・アプリケーションは、ダミー IoT センサのデータを提供する役割も果たします。IoT センサは、Ultralight 構
文でコマンドと測定値を含む HTTP リクエストを出しています。IoT センサのユーザ名とパスワードはすでに **Keycloak** に登録さ
れていますが、プログラムごとに OAuth2 アクセス・トークンを取得し、**IoT Agent** の前にある 2 番目の **APISIX** PEP Proxy
にリクエストします。

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

`tutorial` コンテナは、ダミー Ultralight センサをホストします。以前のすべてのチュートリアルに示されているように、**IoT
Agent** にポート `7896` で直接アクセスするのではなく、すべてのトラフィックが、`iot-agent-proxy` の ポート `7897` に転送
されます。関連する `tutorial` コンテナの設定のほとんどは、以前のチュートリアルで説明されており、`DUMMY_DEVICES_USER` お
よび `DUMMY_DEVICES_PASSWORD` は新しい追加項目です。

| キー                    | 値                                                | 説明                                                                                                                              |
| ----------------------- | ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| IOTA_HTTP_HOST          | `iot-agent-proxy`                                 | Ultra Light 2.0 用 IoT Agent を保護する APISIX PEP Proxy のホスト名                                                                |
| IOTA_HTTP_PORT          | `7896`                                            | IoT Agent を保護する APISIX PEP Proxy がリスンしているポート                                                                       |
| DUMMY_DEVICES_PORT      | `3001`                                            | ダミー IoT デバイスがコマンドを受信するために使用するポート                                                                       |
| DUMMY_DEVICES_TRANSPORT | `HTTP`                                            | ダミー IoT デバイスによって使用されるデフォルトのトランスポート                                                                   |
| DUMMY_DEVICES_API_KEY   | `4jggokgpepnvsb2uv4s40d59ov`                      | UltraLight インタラクションに使用されるランダムなセキュリティキー - デバイスと IoT Agent 間のインタラクションの完全性を保証します |
| DUMMY_DEVICES_USER      | `iot_sensor_00000000-0000-0000-0000-000000000000` | **Keycloak** のデバイスに割り当てられたユーザ名                                                                                    |
| DUMMY_DEVICES_PASSWORD  | `test`                                            | **Keycloak** のデバイスに割り当てられたパスワード                                                                                  |

`DUMMY_DEVICES_USER` および `DUMMY_DEVICES_PASSWORD` は、通常、**Keycloak** のアプリケーションに新しいエントリを追加する
ことで得られますが、このチュートリアルでは **PostgreSQL** データベースに起動時のデータを入力することで事前定義されています。

<a name="securing-south-port-traffic---start-up"></a>

## サウス・ポート・トラフィックの保護 - 起動

**Orion-LD** と **IoT Agent** の両方へのアクセスを保護する PEP Proxies を使用してシステムを起動するには、次のコマンドを
実行します :

```console
./services southport
```

<a name="iot-sensor-logs-in-to-the-application-using-the-rest-api"></a>

## IoT センサが REST API を使用してアプリケーションにログイン

<a name="keyrock---iot-sensor-obtains-an-access-token"></a>

### Keycloak - IoT センサによるアクセス・トークンの取得

IoT センサとしてのログインは、ユーザと同じユーザ・クレデンシャル・フローに従います。ログインしてパスワード `test` でセン
サ `iot_sensor_00000000-0000-0000-0000-000000000000` を特定するには、`grant_type=password` で `oauth2/token` エンドポイ
ントを使って **Keycloak** に POST リクエストを送ります :

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

この例では、デバイス `motion001` からの保護されたリクエストをシミュレートします。

Ultralight IoT Agent の前にある PEP Proxy への POST リクエストは、事前にプロビジョニングされたリソース `iot/d` エンドポ
イントを識別し、デバイス `motion001` の測定値を渡します。`Authorization` ヘッダを追加すると、リクエスト元が Keycloak に登
録されていると識別され、測定が IoT Agent 自体に正常に渡されます。

#### :one::six: リクエスト:

```console
curl -X POST \
  'http://localhost:1030/iot/iot/d?k=4jggokgpepnvsb2uv4s40d59ov&i=motion001' \
  -H 'Authorization: {{access_token}}' \
  -H 'Content-Type: text/plain' \
  -d 'c|1'
```

<a name="securing-south-port-traffic---sample-code"></a>

## サウス・ポート・トラフィックの保護 - サンプル・コード

IoT センサが起動すると、他のユーザと同様にログインしてアクセス・トークンを取得する必要があります :

```javascript
const DUMMY_DEVICE_HTTP_HEADERS = { "Content-Type": "text/plain" };
```

```javascript
function initSecureDevices() {
    Security.oa
        .getOAuthPasswordCredentials(process.env.DUMMY_DEVICES_USER, process.env.DUMMY_DEVICES_PASSWORD)
        .then((results) => {
            DUMMY_DEVICE_HTTP_HEADERS["Authorization"] = results.access_token;
            return;
        })
        .catch((error) => {
            debug(error);
            return;
        });
}
```

その後、各 HTTP リクエストには、IoT センサを識別するリクエストに `Authorization` ヘッダを含みます :

```javascript
const options = {
    method: "POST",
    url: UL_URL,
    qs: { k: UL_API_KEY, i: deviceId },
    headers: DUMMY_DEVICE_HTTP_HEADERS,
    body: state,
};

request(options, (error) => {
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

`iot-agent` コンテナはポート `4041` でリッスンしており、ポート `1027` で `orion-proxy` にトラフィックを転送するように設
定されています。

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

| キー                      | 値                                     | 説明                                                     |
| ------------------------- | -------------------------------------- | -------------------------------------------------------- |
| IOTA_AUTH_ENABLED         | `true`                                 | ノース・ポートで認証を使用するかどうか                   |
| IOTA_AUTH_TYPE            | `oauth2`                               | 使用する承認のタイプ (Keycloak は OAuth2 を使用します)    |
| IOTA_AUTH_HEADER          | `Authorization`                        | リクエストに追加されるヘッダの名前                       |
| IOTA_AUTH_HOST            | `keyrock`                              | アプリケーションを保持する Identity Manager              |
| IOTA_AUTH_PORT            | `3005`                                 | Identity Manager がリッスンしているポート                |
| IOTA_AUTH_URL             | `http://keyrock:3005`                  | 認証要求の URL                                           |
| IOTA_AUTH_CLIENT_ID       | `tutorial-dckr-site-0000-xpresswebapp` | Keycloak 内のアプリケーションの Id                        |
| IOTA_AUTH_CLIENT_SECRET   | `tutorial-dckr-host-0000-clientsecret` | Keycloak 内のアプリケーションのクライアント・シークレット |
| IOTA_AUTH_PERMANENT_TOKEN | `true`                                 | 永久トークンを使用するかどうか                           |
| IOTA_AUTH_TOKEN_PATH      | `/oauth2/token`                        | トークンを要求するときに使用されるパス                   |

<a name="securing-an-iot-agent-north-port---start-up"></a>

## IoT Agent ノース・ポートの保護 - 起動

**Orion-LD** と **IoT Agent** ノース・ポート間のアクセスを保護する PEP Proxy でシステムを起動するには、次のコマンドを実
行します :

```console
./services northport
```

<a name="keyrock---obtaining-a-permanent-token"></a>

### Keycloak - 永久トークンの取得

Keycloak アプリケーションは、永久トークンを提供するように構成されています。

標準の `Authorization: Basic` ヘッダは、クライアント ID とシークレットの base 64 連結を保持します。パラメータ
`scope=permanent` が追加され、利用可能な場合に永続トークンを取得します。レスポンスには、デバイスのプロビジョニングに使用
できる `access_token` が含まれています。

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

アクセス・トークン (トラスト・トークンとも呼ばれる) をサービス・グループに追加する必要があります。

#### :one::eight: リクエスト:

```console
curl -iX POST \
  'http://localhost:4041/iot/services' \
  -H 'Content-Type: application/json' \
  -H 'fiware-service: openiot' \
  -H 'fiware-servicepath: /' \
  -d '{
 "services": [
   {
     "apikey":      "4jggokgpepnvsb2uv4s40d59ov",
     "cbroker":     "http://orion:1026",
     "entity_type": "Motion",
     "resource":    "/iot/d",
     "trust": "e37aeef5d48c9c1a3d4adf72626a8745918d4355"
   }
 ]
}'
```

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
