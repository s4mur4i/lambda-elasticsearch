#!/bin/bash
aws cloudformation deploy --template-file cloudformation/template.json --stack-name json-event --capabilities CAPABILITY_IAM
rm service.zip
cd lambda
zip -X -r "../service.zip" *
cd ..
aws lambda update-function-code --function-name json-event-handler --zip-file fileb://service.zip
