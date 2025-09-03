create database ExercicioAula10012024

use ExercicioAula10012024


Create table Cliente (
id int identity (1,1),
nome varchar(50),
primary key (id)
);


create table Venda(
id int identity (1,1),
cliente int,
FOREIGN KEY (cliente) REFERENCES Cliente(id),
dataVenda date,
desconto decimal(4,2),
produto int,
FOREIGN KEY (produto) REFERENCES Produto(id), 
quantidade int,
PRIMARY KEY (id)
);


create table Produto(
id int identity (1,1),
nome varchar(50)
PRIMARY KEY (id)
);

create table Stock(
produto int,
FOREIGN KEY (produto) REFERENCES Produto (id),
stock int
PRIMARY KEY (produto)
);

create table Preco(
id int identity (1,1),
produto int,
FOREIGN KEY (produto) REFERENCES Produto(id),
data_preco datetime,
preco decimal (10,2)
PRIMARY KEY (id)
);

select * from Cliente
select * from Venda
select * from Produto
select * from Preco
select * from Stock

insert into Cliente values
('Ana'), ('Manuel'), ('joão'), ('Filipe'), ('Catarina'), ('Xana'), ('Zeca')
insert into Produto values
('Materlo'), ('Arroz'), ('Serrote'), ('Prego'), ('Farinha'), ('Cenas')

insert into Stock values (
(select id from Produto where nome='Materlo'), 10);
insert into Stock values (
(select id from Produto where nome='Arroz'), 8);
insert into Stock values (
(select id from Produto where nome='Serrote'), 6);
insert into Stock values (
(select id from Produto where nome='Prego'), 4);
insert into Stock values (
(select id from Produto where nome='Farinha'), 2);
insert into Stock values (
(select id from Produto where nome='Cenas'), 50);

insert into Preco values (
(select id from Produto where nome='Materlo'), '2024-01-10', 10.4)
insert into Preco values (
(select id from Produto where nome='Materlo'), '2024-01-09', 8.4)
insert into Preco values (
(select id from Produto where nome='Serrote'), '2024-01-08', 6.2)
insert into Preco values (
(select id from Produto where nome='Prego'), '2024-01-07', 100.2)
insert into Preco values (
(select id from Produto where nome='Farinha'), '2024-01-06', 5.12)
insert into Preco values (
(select id from Produto where nome='Cenas'), '2024-01-05', 10.10)

--) View para retirar a ultima data de todos os precos
GO
Create view UltimaData as
select produto, MAX(data_preco) as maxData
from Preco
Group by produto
GO

select * from UltimaData



--) View para ver os produtos e ultimos precos 
GO
create view precosAtuais as
select pr.produto, pr.preco, pr.data_preco
from Preco pr
INNER JOIN UltimaData u
on pr.produto=u.produto and pr.data_preco=u.maxData
GO

select * from precosAtuais



--) View para ver todos os produtos com preço e com stock
GO
create view produtosComPreco_eStock as 
select p.nome, pr.preco, s.stock
from Produto p
inner join precosAtuais pr
on p.id=pr.produto
left join Stock s
on p.id=s.produto
GO

select * from produtosComPreco_eStock
select * from Produto
Select * from Preco
select * from Stock

update Stock
set stock=0
where produto=4
