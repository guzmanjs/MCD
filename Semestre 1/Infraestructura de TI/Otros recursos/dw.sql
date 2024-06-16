--Create Customer dimension table in Data Warehouse which will hold customer personal details.
Create table DimCustomer
(
CustomerID int primary key,
CustomerAltID varchar(10) not null,
CustomerName varchar(50),
Gender varchar(20)
);

--Create sequence and trigger to generate surrogate key for Customer dimension table.
Create sequence DimCustomerSeq
start with 1
increment by 1
minvalue 1
maxvalue 999999999999999999999999999;

create or replace trigger DimCustomerSeqTrigger
before insert on DimCustomer
for each row
    when (new.CustomerID is null)
begin
    :new.CustomerID := DimCustomerSeq.NEXTVAL;
end;
/         

--Create basic level of Product Dimension table without considering any Category or Subcategory
Create table DimProduct(
ProductKey int primary key,
ProductAltKey varchar(10)not null,
ProductName varchar(100),
ProductActualCost Numeric(10,2),
ProductSalesCost Numeric(10,2)
);

--Create sequence and trigger to generate surrogate key for Product dimension table.
Create sequence DimProductSeq
start with 1
increment by 1
minvalue 1
maxvalue 999999999999999999999999999;

create or replace trigger DimProductSeqTrigger
before insert on DimProduct
for each row
    when (new.ProductKey is null)
begin
    :new.ProductKey := DimProductSeq.NEXTVAL;
end;        
/

--Create Store Dimension table which will hold details related stores available across various places.
Create table DimStores(
StoreID int primary key,
StoreAltID varchar(10)not null,
StoreName varchar(100),
StoreLocation varchar(100),
City varchar(100),
State varchar(100),
Country varchar(100)
);

--Create sequence and trigger to generate surrogate key for Product dimension table.
Create sequence DimStoresSeq
start with 1
increment by 1
minvalue 1
maxvalue 999999999999999999999999999;

create or replace trigger DimStoresSeqTrigger
before insert on DimStores
for each row
    when (new.StoreID is null)
begin
    :new.StoreID := DimStoresSeq.NEXTVAL;
end;
/
--Create Dimension Sales Person table which will hold details related stores available across various places.
Create table DimSalesPerson(
SalesPersonID int primary key,
SalesPersonAltID varchar(10)not null,
SalesPersonName varchar(100),
StoreID int,
City varchar(100),
State varchar(100),
Country varchar(100)
);

--Create sequence and trigger to generate surrogate key for Sales Person dimension table.
Create sequence DimSalesPersonSeq
start with 1
increment by 1
minvalue 1
maxvalue 999999999999999999999999999;

create or replace trigger DimSalesPersonSeqTrigger
before insert on DimSalesPerson
for each row
    when (new.SalesPersonID is null)
begin
    :new.SalesPersonID := DimSalesPersonSeq.NEXTVAL;
end;
/


--Fill the Customer dimension with sample Values
Insert into DimCustomer(CustomerAltID,CustomerName,Gender)values ('IMI-001','Henry Ford','M');
Insert into DimCustomer(CustomerAltID,CustomerName,Gender)values ('IMI-002','Bill Gates','M');
Insert into DimCustomer(CustomerAltID,CustomerName,Gender)values ('IMI-003','Muskan Shaikh','F');
Insert into DimCustomer(CustomerAltID,CustomerName,Gender)values ('IMI-004','Richard Thrubin','M');
Insert into DimCustomer(CustomerAltID,CustomerName,Gender)values ('IMI-005','Emma Wattson','F');

--Fill the Product dimension with sample Values
Insert into DimProduct(ProductAltKey,ProductName, ProductActualCost, ProductSalesCost)values('ITM-001','Wheat Floor 1kg',5.50,6.50);
Insert into DimProduct(ProductAltKey,ProductName, ProductActualCost, ProductSalesCost)values('ITM-002','Rice Grains 1kg',22.50,24);
Insert into DimProduct(ProductAltKey,ProductName, ProductActualCost, ProductSalesCost)values('ITM-003','SunFlower Oil 1 ltr',42,43.5);
Insert into DimProduct(ProductAltKey,ProductName, ProductActualCost, ProductSalesCost)values('ITM-004','Nirma Soap',18,20);
Insert into DimProduct(ProductAltKey,ProductName, ProductActualCost, ProductSalesCost)values('ITM-005','Arial Washing Powder 1kg',135,139);

--Fill the Store Dimension with sample Values
Insert into DimStores(StoreAltID,StoreName,StoreLocation,City,State,Country )values ('LOC-A1','X-Mart','S.P. RingRoad','Ahmedabad','Guj','India');
Insert into DimStores(StoreAltID,StoreName,StoreLocation,City,State,Country )values ('LOC-A2','X-Mart','Maninagar','Ahmedabad','Guj','India');
Insert into DimStores(StoreAltID,StoreName,StoreLocation,City,State,Country )values ('LOC-A3','X-Mart','Sivranjani','Ahmedabad','Guj','India');

--Fill the Dimension Sales Person with sample values:
Insert into DimSalesPerson(SalesPersonAltID,SalesPersonName,StoreID,City,State,Country )values ('SP-DMSPR1','Ashish',1,'Ahmedabad','Guj','India');
Insert into DimSalesPerson(SalesPersonAltID,SalesPersonName,StoreID,City,State,Country )values ('SP-DMSPR2','Ketan',1,'Ahmedabad','Guj','India');
Insert into DimSalesPerson(SalesPersonAltID,SalesPersonName,StoreID,City,State,Country )values ('SP-DMNGR1','Srinivas',2,'Ahmedabad','Guj','India');
Insert into DimSalesPerson(SalesPersonAltID,SalesPersonName,StoreID,City,State,Country )values ('SP-DMNGR2','Saad',2,'Ahmedabad','Guj','India');
Insert into DimSalesPerson(SalesPersonAltID,SalesPersonName,StoreID,City,State,Country )values ('SP-DMSVR1','Jasmin',3,'Ahmedabad','Guj','India');
Insert into DimSalesPerson(SalesPersonAltID,SalesPersonName,StoreID,City,State,Country )values ('SP-DMSVR2','Jacob',3,'Ahmedabad','Guj','India');



--Facts Table
--Facts Table
Create Table FactProductSales(
TransactionId int primary key,
SalesInvoiceNumber int not null,
StoreID int not null,
CustomerID int not null,
ProductID int not null,
SalesPersonID int not null,
Quantity float,
SalesTotalCost Numeric(10,2),
ProductActualCost Numeric(10,2),
SalesTimeKey int,
Deviation float
);
--Create sequence and trigger to generate surrogate key for Facts table.
Create sequence FactsSeq
start with 1
increment by 1
minvalue 1
maxvalue 999999999999999999999999999;

create or replace trigger FactProductSalesSeqTrigger
before insert on FactProductSales
for each row
    when (new.TransactionId is null)
begin
    :new.TransactionId := FactsSeq.NEXTVAL;
end;
/

-- Add relation between fact table foreign keys to Primary keys of Dimensions
AlTER TABLE FactProductSales ADD CONSTRAINT 
FK_StoreID FOREIGN KEY (StoreID)REFERENCES DimStores(StoreID);
AlTER TABLE FactProductSales ADD CONSTRAINT 
FK_CustomerID FOREIGN KEY (CustomerID)REFERENCES Dimcustomer(CustomerID);
AlTER TABLE FactProductSales ADD CONSTRAINT 
FK_ProductKey FOREIGN KEY (ProductID)REFERENCES Dimproduct(ProductKey);
AlTER TABLE FactProductSales ADD CONSTRAINT 
FK_SalesPersonID FOREIGN KEY (SalesPersonID)REFERENCES Dimsalesperson(SalesPersonID);

