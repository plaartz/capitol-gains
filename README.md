# Capitol Gains - Politician Trade Tracker

## Team Name
Capitol Gains

## Project Abstract
Capitol Gains is developing a platform for tracking American politicians' stock trades, ensuring transparency and enabling the public to make informed decisions. The platform will pull data from the Financial Disclosure website where politicians report their trades. The data will be presented in an easy-to-navigate interface using Python (Django) on the backend with a MySQL database, and React on the frontend. This platform allows users to monitor stock trades, compare trading activity, and model their own investment decisions based on the activity of their favorite politicians, aiming to mirror the functionality of Capitol Trades.

## Customer
Capitol Gains is primarily being developed for our professor and TAs to meet the project requirements. In the broader scope, the platform is designed for the public who want to keep up-to-date on politician stock trades. The goal is to provide transparency in political stock transactions and help users model their own trades based on these reports, fostering accountability and fair access to financial information.

## Specification

### Technology Stack
The project uses the following technology stack:

```mermaid
flowchart RL
subgraph Front End
	A(Javascript: React)
end
	
subgraph Back End
	B(Python: Django with \nDjango Rest Framework)
end
	
subgraph Database
	C[(MySQL)]
end

A <-->|"REST API"| B
B <-->|Django ORM| C
```

### Database Architecture
Our database will store information about politicians, the stocks they trade, and the companies associated with those stocks. Below is an initial draft of the ER diagram:

```mermaid
erDiagram
    Politician ||--o{ Trade : "makes"
    Trade ||--o{ Stock : "involves"
    Stock ||--o{ Company : "issued by"

    Politician {
        int politician_id PK
        string name
        string party
        string state
    }

    Trade {
        int trade_id PK
        int politician_id FK
        int stock_id FK
        string trade_date
        string transaction_type
        decimal trade_amount
    }

    Stock {
        int stock_id PK
        int company_id FK
        string ticker_symbol
        string stock_name
    }

    Company {
        int company_id PK
        string company_name
        string industry
    }
```

Further details on database relationships and schema will be provided as development progresses.

### Flowchart
This flowchart describes how the system processes user interactions and data flows from the frontend to the backend and database:

```mermaid
graph TD;
    Start([User Request]) --> Fetch_Data[/Fetch Politician Trade Data/];
    Fetch_Data --> Process_Data[Process Trade Data];
    Process_Data --> Save_Data[Save to MySQL Database];
    Save_Data --> Generate_Response[Generate JSON Response];
    Generate_Response --> Display_Response[/Display Trade Data to User/];
    Display_Response --> End([End]);
```

## Behavior
The behavior of the system is modeled using the following state diagram, which will evolve as the project develops:

```mermaid
stateDiagram
    [*] --> Ready
    Ready --> FetchingData : Request for Trade Data
    FetchingData --> Ready : Data Fetched Successfully
    FetchingData --> Error : Data Fetch Error
    Error --> Ready : Retry Fetch
```

## Sequence Diagram
The interaction between the frontend, backend, and database is captured in this sequence diagram. This diagram shows how user requests will be processed:

```mermaid
sequenceDiagram

participant ReactFrontend
participant DjangoBackend
participant MySQLDatabase

ReactFrontend ->> DjangoBackend: HTTP Request (e.g., GET /api/data)
activate DjangoBackend

DjangoBackend ->> MySQLDatabase: Query (e.g., SELECT * FROM data_table)
activate MySQLDatabase

MySQLDatabase -->> DjangoBackend: Result Set
deactivate MySQLDatabase

DjangoBackend -->> ReactFrontend: JSON Response
deactivate DjangoBackend
```

## Standards & Conventions
Our coding standards and conventions follow established guidelines to maintain consistency and code quality across the project.

You can refer to the [Style Guide & Conventions](STYLE.md) document for detailed information on code formatting, naming conventions, and other best practices.

## Testing Strategy
We will use **JUnit 5** for our testing framework to ensure the backend's reliability and functionality. Unit tests and integration tests will be written to cover key functions of the system.

## Deployment Strategy
We will use **Docker** for containerizing the application, ensuring consistent environments across development and production. Additionally, we plan to deploy using cloud services (AWS or Azure, yet to be determined) for hosting our application and managing the MySQL database.

## Known Issues & Future Features
Currently, there are no major known issues. Future features might include advanced filtering options, user notifications for new trades, and the ability to track specific politicians or stocks.