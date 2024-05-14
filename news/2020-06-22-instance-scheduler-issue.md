---
title: AWS Instance scheduler troubleshooting information
description: AWS Instance scheduler troubleshooting information
slug: 2020-06-22-instance-scheduler-issue
authors:
  - name: CEC
    title: CEC team
    url: https://gio-tech-guides.apps.airliquide.com
    image_url: img/news_author/user_1.png
badge: Operations
image: img/news_logo/aws_1.png
tags: [aws]
hide_table_of_contents: false
---

We are still working with AWS to permanently fix the AWS Instance Scheduler issue that is tracked under PRB0041987. We have planned [CHG0104534](https://airliquide.service-now.com/nav_to.do?uri=%2Fchange_request.do%3Fsys_id%3D7bd7fe371b1510500faedc6a9b4bcb8f%26sysparm_stack%3D%26sysparm_view%3D) on June 23rd to reenable the solution without impacting your workloads.  

On this date, starting 2PM CET, we will temporarily modify the "Schedule" tag key for all resources to disable the service for all EC2 and RDS instances in AWS Essential and Managed accounts. You must get in touch with us if you have deployed your own instance of the AWS Instance Scheduler so that we can discard your accounts from this change.
