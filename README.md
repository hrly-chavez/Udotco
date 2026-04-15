# System About

The system is a comprehensive enterprise resource planning (ERP) platform tailored for the land transportation sector, designed to centralize fleet management, maintenance logistics, and procurement cycles. At its structural core is a high-integrity PostgreSQL database, featuring a relational data model that links physical assets—such as buses and inventory—to dynamic operational workflows. This architecture ensures real-time synchronization between vehicle health records, material stock levels, and financial procurement status, providing a single source of truth for the company’s entire fleet lifecycle.

The platform orchestrates a sophisticated multi-role workflow that bridges the gap between field operations and administrative oversight. Through a secure access control layer, Drivers initiate the maintenance cycle by submitting digital requests for assigned units, which are instantly routed to the Mechanic’s dashboard. The system enables Mechanics to manage the end-to-end repair process, from tracking labor hours to recording specific material consumption. This is deeply integrated with an automated Inventory Module; if required parts are unavailable, the system triggers a structured procurement workflow, generating purchase requests that move directly to the Finance department for supplier coordination and purchase order processing.

Developed using Django, HTML, and Bootstrap, the system replaces fragmented manual logs with a streamlined, automated pipeline. By guiding every action through a predefined status-flow—from initial issue reporting to maintenance completion and part replenishment—the platform significantly enhances operational efficiency. The result is a robust management tool that not only reduces vehicle downtime through faster maintenance turnarounds but also provides a transparent audit trail for inventory usage and procurement spending.







Udotco System (How to start)

TODO: check settings for database connection

1. Create new Virtual Environment
2. Activate venv
3. pip install the requirements
4. migrate and migrations
5. Create superuser
6. Login as admin -> create departments with exact text
    (finance department,
     vehicle maintenance department,
     i.t. department,
     transportation department,)
7. Create Employee and designate them in departments
8. Create Accounts
9. Finish


