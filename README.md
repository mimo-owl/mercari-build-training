# Build@Mercari Training Program

This is mimo-owl's build training repository.

## How to launch Simple Mercari on your PC

### Start Docker
Get a docker image by executing:
```bash
docker pull ghcr.io/mimo-owl/mercari-build-training:step8
```
Then, run docker by executing:
```bash
docker run -d -p 9000:9000 ghcr.io/mimo-owl/mercari-build-training:step8
```
You will be at
```bash
/app #
```
You are now in the docker  container!
In the different window, execute `docker ps`.
You should see a docker image named as `ghcr.io/mimo-owl/mercari-build-training:step8`. Confirm that you see CONTAINER ID.
Notes:
When temporarily exiting the docker, execute `docker stop <CONTAINER ID>`.
When restarting the docker, execute `docker ps -a` to confirm you have the docker image.
Then restart your docker by executing: `docker start <CONTAINER ID>`.
To enter the docker container, execute: `docker exec -it <CONTAINER ID> sh`.
You are now in the docker again!

### Launch App
Install node. Then check your node version by execution `node -v`.
If the version is higher than v22, skip the next step. If not, ensure you get >v22 with the following:
1. Check PATH
Check where you installed node by executing `which -a node`. Example output is:
```bash
/usr/local/bin/node
```
Then, execute:
```bash
echo $PATH
```
Now, you will see `/usr/local/bin/node` is not in there. You have to add the PATH by executing:
```bash
export PATH="/usr/local/bin:$PATH"
```
Now, execute `node -v`. You will successfully see `v22.14.0` (or a higher version). You are all set!

2. Launch the App
Move to directory `typescript/simple-mercari-web` by executing `cd typescript/simple-mercari-web`.
Install necessary library by executing `npm ci`.
Then, launch the app with the following command:
```bash
npm start
```
Visit `http://localhost:3000/` from your browser.
You should now see the Simple Mercari!




Build trainingの前半では個人で課題に取り組んでもらい、Web開発の基礎知識をつけていただきます。
ドキュメントには詳細なやり方は記載しません。自身で検索したり、リファレンスを確認したり、チームメイトと協力して各課題をクリアしましょう。

ドキュメントには以下のような記載があるので、課題を進める際に参考にしてください。

In the first half of Build@Mercari program, you will work on individual tasks to understand the basics of web development. Detailed instructions are not given in each step of the program, and you are encouraged to use official documents and external resources, as well as discussing tasks with your teammates and mentors.

The following icons indicate pointers for

**:book: Reference**

* そのセクションを理解するために参考になるUdemyやサイトのリンクです。課題内容がわからないときにはまずReferenceを確認しましょう。
* Useful links for Udemy courses and external resources. First check those references if you are feeling stuck.

**:beginner: Point**

* そのセクションを理解しているかを確認するための問いです。 次のステップに行く前に、**Point**の問いに答えられるかどうか確認しましょう。
* Basic questions to understand each section. Check if you understand those **Points** before moving on to the next step.

## Tasks

- [x] **STEP1** Git ([JA](document/01-git.ja.md)/[EN](document/01-git.en.md))
- [x] **STEP2** Setup environment ([JA](document/02-local-env.ja.md)
  /[EN](document/02-local-env.en.md))
- [x] **STEP3** Algorithms and Data Structures([JA](document/03-algorithm-and-data-structure.ja.md)/[EN](document/03-algorithm-and-data-structure.en.md))
- [x] **STEP4** Develop API ([JA](document/04-api.ja.md)
  /[EN](document/04-api.en.md))
- [x] **STEP5** Database ([JA](document/05-database.ja.md)/[EN](document/05-database.en.md))
- [x] **STEP6** Writing Tests ([JA](document/06-testing.ja.md)/[EN](document/06-testing.en.md))
- [x] **STEP7** Docker ([JA](document/07-docker.ja.md)/[EN](document/07-docker.en.md))
- [x] **STEP8** Continuous Integration(CI) ([JA](document/08-ci.ja.md)
  /[EN](document/08-ci.en.md))
- [x] **STEP9** (Stretch) Frontend ([JA](document/09-frontend.ja.md)
  /[EN](document/09-frontend.en.md))
- [ ] **STEP10** (Stretch)  Run multi service ([JA](document/10-docker-compose.ja.md)
  /[EN](document/10-docker-compose.en.md))
- [ ] **EXTRA1** (Stretch)  Data Analysis ([Link](document/extra-01-data-analysis.md))

### Other documents

- 効率的に開発できるようになるためのTips / Tips for efficient development ([JA](document/tips.ja.md)/[EN](document/tips.en.md))

### Which one should I choose, Python or Go?

* Mercari uses Go for building the backend of their applications. If you like taking on challenges, using Go will let you develop in an environment similar to Mercari's.
* Python is a relatively easy-to-write programming language. Choosing Python may make it easier for you to understand the overall flow.


* MercariではBackend開発にGoを利用しています。挑戦できそうな方はこちらを選んでいただくとよりMercariに近い環境で開発いただけます。
* Pythonは比較的簡単にかけるプログラミング言語です。Pythonを選んだほうが全体のフローの理解がしやすいかと思われます。

