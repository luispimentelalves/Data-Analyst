create database PL09;

use PL09;

create table Receitas(
	data date,
	hora time,
	chefe int,
	nome varchar(50),
	titulo varchar(50),
	descricao varchar(MAX),
	primary key (data,hora,chefe)
);

insert into Receitas values
('2004-02-01','12:23:00','56','Paulo Perdiz','Bolo Noz','O bolo é feito com 250 gramas de...'),
('2004-05-02','17:55:00','71','Alexandre Mota','Pudim Flan','Primeiramente, coloca-se a forma...'),
('2004-05-06','18:12:00','56','Paulo Perdiz','Bolo Chocolate','A forma de confecionar o bolo é a seguinte...'),
('2004-04-02','19:11:00','81','António Pereira','Doces Casa','Os doces são feitos sempre com...');

select * from Receitas;

---------------------------------------------------
---     Ultimas 3 Receitas de um Dado Chefe     ---
---------------------------------------------------
create procedure U3Receitas_DadoChefe(
	@chefe int 
)
as
begin
	select top(3) titulo from Receitas
	where chefe = @chefe order by data desc
end

Exec U3Receitas_DadoChefe @chefe = 71

---------------------------------------------------
---     Ultimas 3 Receitas de Vários Chefes     ---
---------------------------------------------------
create type ListInt As Table (valor int); --Criar Tipo []

create procedure U3Receitas_ListaChefes(
	@chefes ListInt READONLY 
)
as
begin
	select top(3) titulo
	from Receitas
	where chefe in (select valor from @chefes)
	order by data desc
end

SET NOCOUNT ON
Declare @listaChefes ListInt; -- Variável(list/tabela) desse tipo []
insert into @listaChefes (valor) Values (71), (81); --arr = [56,71]
Exec U3Receitas_ListaChefes @chefes = @listaChefes

---------------------------------------------------
---     Ultimas 3 Receitas de 2 Chefes          ---
---------------------------------------------------
create procedure U3Receitas_Dados2Chefe(
	@chefe1 int,
	@chefe2 int
)
as
begin
	select top(3) titulo from Receitas
	where chefe = @chefe1 or chefe = @chefe2
	order by data desc
end

Exec U3Receitas_Dados2Chefe @chefe1 = null, @chefe2 = 71

--------------------------------------------------------------------
---     Ultimas 3 Receitas de um Dado Chefe de Dada Descricao    ---
--------------------------------------------------------------------
drop procedure U3Receitas_DadoChefe_DadaDesc;
create procedure U3Receitas_DadoChefe_DadaDesc(
	@chefe int,
	@descricao varchar(MAX)
)
as
begin
	select top(3) titulo from Receitas
	where chefe like concat('%',@chefe,'%') and descricao like concat('%',@descricao,'%')
	order by data desc
end

Exec U3Receitas_DadoChefe_DadaDesc @chefe = null, @descricao='a'

-----------------------------------------------------------------------------
---   Ultimas 3 Receitas de um Dado Chefe de Dada Descricao 2 (com if)    ---
-----------------------------------------------------------------------------
drop procedure U3Receitas_DadoChefe_DadaDesc2;
create procedure U3Receitas_DadoChefe_DadaDesc2(
	@chefe int,
	@descricao varchar(MAX)
)
as
begin
	if @chefe is null
	begin
		select top(3) titulo from Receitas
		where descricao like concat('%',@descricao,'%')
		order by data desc
	END 
	else
	begin
		select top(3) titulo from Receitas
		where chefe = @chefe and descricao like concat('%',@descricao,'%')
		order by data desc
	END 
end

Exec U3Receitas_DadoChefe_DadaDesc2 @chefe = 56, @descricao='a'

select * from Receitas;



















