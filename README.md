# media-analysis

## Chrome Extension Quick Start 
1. Drag the `chrome-extension` folder onto the page at chrome://extensions to install (nice gif / instructions here: [https://blog.lateral.io/2016/04/create-chrome-extension-modify-websites-html-css/](https://blog.lateral.io/2016/04/create-chrome-extension-modify-websites-html-css/)
2. Go to EC2 on AWS: [https://us-east-2.console.aws.amazon.com/ec2/v2/home?region=us-east-2#Instances:sort=instanceState](https://us-east-2.console.aws.amazon.com/ec2/v2/home?region=us-east-2#Instances:sort=instanceState) 
3. Click Actions -> Instance State -> Start
4. Click Connect
5. update `HEADLINES_SERVER_REQUEST_URL` in `chrome-extension/content.js` with the new public dns
6. go to [chrome://extensions](chrome://extensions) and hit update
6. connect to the ec2 instance using the provided ssh command (slack me if you need justin.pem)
7. once logged on to ec2, `cd ~/headlines && bash setup.sh`
8. if successful, you should see a help message at the public dns (should be a url like `http://ec2-18-221-33-195.us-east-2.compute.amazonaws.com/`)
