### Steps

- Create project on gitlab.
- Get projet from gitlab with git clone http://oauth2:glpat-bAMj-tBqsP-TKpDf1O1dpW86MQp1OjEH.01.0w15puzey@<project_address>
- Add source code inside the project (From skeleton).
- Make new commit
    ```bash
    git add .
    git commit -am "description of commit"
    git push origin main
    ```

- create new project inside sonarqube
- get sonar project information from sonarqube (host, token, project-key, project-name)
- update .gitlab-ci.yml inside your project
- make new commit and push