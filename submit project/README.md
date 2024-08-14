## Monthly Cost Analysis
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

| Azure Resource | Service Tier | Monthly Cost |
| ------------ | ------------ | ------------ |
| *Azure Postgres Database* | Burstable (1-20 vCores) + Standard_B1ms (1 vCore, 2 GiB memory, 640 max iops) + Storage selected 128 GiB (USD 0.14 per GiB) |       USD 36.64       |
| *Azure Service Bus*   |    Basic     |     0.05 USD      |
| *Azure Web App*   |  Linux OS (Basic Tier B1)     |     13.14 USD    |
| *Azure Function App*   |    400,000 GB-s     |     0       |
| *Total*   |         |     49.83      |


## Architecture Explanation
This is a placeholder section where you can provide an explanation and reasoning for your architecture selection for both the Azure Web App and Azure Function.
    ### Answer:
        - With Web App:
            I used the Basic tier with autoscaling becuase app service provides a managed environment with easy scaling options. The basic tier offers a good balance between cost and performance.
            + Detailed Info:
                        App Service plan: ASP-rgproj3-8d70
                        Operating System: Linux
                        SKU and size: Basic (B1)
        - With Azure Function:
            I deployed the Azure Function using the Consumption Plan because the Consumption Plan charges only for per-second resource consumption and executions. It’s ideal for functions that are triggered infrequently, making it highly cost-effective.
            + Detailed Info:
                        App Service plan: SoutheastAsiaLinuxDynamicPlan
                        Operating System: Linux
                        SKU and size: Dynamic Y1
                        Service Tier: Consumption plan
    Detailed Info: After migrating the application web app to an Azure App Service and refactoring the notification logic to an Azure Function via a service bus queue message:
        - Scalable web application to handle varying loads and provides a scalable environment that can automatically adjust resources based on demand, this scalability ensures cost-effectiveness as you only pay for what you use.
        - Once the admin sends a notification, it won't take so long now because now I use Azure Functions with a service bus queue, the notification process is transferred to a serverless. This allows the web application to remain responsive, while the function processes notifications asynchronously, reducing the workload on the web application and ensuring quick delivery of notifications.
        - Current architecture optimized for performance and cost by I combined the app service and Functions allows the application to be cost-effective by optimizing resource. The App Service will ensure the web application runs efficiently, while Functions will allow for scalable, processing of notifications, reducing costs by using resources during actual function execution.

