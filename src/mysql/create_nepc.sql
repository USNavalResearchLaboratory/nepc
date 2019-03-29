DROP DATABASE IF EXISTS `nepc`;
CREATE DATABASE IF NOT EXISTS `nepc`;

SET default_storage_engine = INNODB;

CREATE TABLE `nepc`.`species`(
	`id` INT UNSIGNED NOT NULL auto_increment ,
	`name` VARCHAR(40) NOT NULL ,
	`tex` VARCHAR(100) NOT NULL ,
	PRIMARY KEY(`id`)
);

CREATE TABLE `nepc`.`processes`(
	`id` INT UNSIGNED NOT NULL auto_increment ,
	`name` VARCHAR(40) NOT NULL ,
	`long_name` VARCHAR(240) NOT NULL ,
	`lhs_e` BOOLEAN ,
	`rhs_e` BOOLEAN ,
	`lhs_hv` BOOLEAN ,
	`rhs_hv` BOOLEAN ,
	PRIMARY KEY(`id`)
);

CREATE TABLE `nepc`.`states`(
	`id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
	`specie_id` INT UNSIGNED NOT NULL ,
	`name` VARCHAR(100) NOT NULL ,
	`tex` VARCHAR(100) NOT NULL ,
	`configuration` JSON NOT NULL ,
	PRIMARY KEY(`id`) ,
	INDEX `SPECIE_ID`(`specie_id` ASC) ,
	CONSTRAINT `specie_id_STATES` FOREIGN KEY(`specie_id`) 
		REFERENCES `nepc`.`species`(`id`) 
		ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE `nepc`.`cs`(
	`id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
	`specie_id` INT UNSIGNED NOT NULL ,
	`process_id` INT UNSIGNED NOT NULL ,
	`units_e` DOUBLE NOT NULL,
	`units_sigma` DOUBLE NOT NULL,
	`ref_id` INT UNSIGNED NOT NULL,
	`lhs_id` INT UNSIGNED NULL ,
	`rhs_id` INT UNSIGNED NULL ,
	`hv` DOUBLE NULL ,
	`background` VARCHAR(10000) ,
	`lpu` DOUBLE NULL ,
	`upu` DOUBLE NULL ,
	PRIMARY KEY(`id`) ,
	INDEX `SPECIE_ID`(`specie_id` ASC) ,
	INDEX `PROCESS_ID`(`process_id` ASC) ,
	CONSTRAINT `SPECIE_ID_CS` FOREIGN KEY(`specie_id`)
		REFERENCES `nepc`.`species`(`id`)
		ON DELETE RESTRICT ON UPDATE CASCADE,
	CONSTRAINT `PROCESS_ID_CS` FOREIGN KEY(`process_id`)
		REFERENCES `nepc`.`processes`(`id`)
		ON DELETE RESTRICT ON UPDATE CASCADE,
	CONSTRAINT `LHS_ID_CS` FOREIGN KEY(`lhs_id`)
		REFERENCES `nepc`.`states`(`id`),
	CONSTRAINT `RHS_ID_CS` FOREIGN KEY(`rhs_id`)
		REFERENCES `nepc`.`states`(`id`)
);
/*
*/

CREATE TABLE `nepc`.`csdata`(
	`id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
	`cs_id` INT UNSIGNED NOT NULL ,
	`e` DOUBLE NOT NULL ,
	`sigma` DOUBLE NOT NULL ,
	PRIMARY KEY(`id`) ,
        INDEX `CS_ID`(`cs_id` ASC) ,
        CONSTRAINT `CS_ID_CSDATA` FOREIGN KEY(`cs_id`)
                REFERENCES `nepc`.`cs`(`id`)
                ON DELETE RESTRICT ON UPDATE CASCADE
);
	

/***************/
/** Load data **/
/***************/
LOAD DATA LOCAL INFILE 'processes.tex'    
	INTO TABLE nepc.processes
	FIELDS TERMINATED BY '\&' ESCAPED BY ''
	LINES TERMINATED BY '\\\\\n' STARTING BY ''
	IGNORE 2 LINES;

LOAD DATA LOCAL INFILE 'species.txt' 
	INTO TABLE nepc.species;

LOAD DATA LOCAL INFILE 'states.tex'    
	INTO TABLE nepc.states
	FIELDS TERMINATED BY '\&' ESCAPED BY ''
	LINES TERMINATED BY '\\\\\n' STARTING BY ''
	IGNORE 3 LINES
	(id,@o1,@o2,@o3,@o4,@o5,@o6,name,tex)
	/*TODO: refactor to read orbitals from tex file or vice versa*/
	SET configuration = JSON_OBJECT(
		JSON_OBJECT('order', 
			JSON_ARRAY("2sigma_u", '1pi_u', '3sigma_g', '1pi_g', '3sigma_u', '3ssigma_g')
		),
		JSON_OBJECT('occupations',
			JSON_OBJECT(
				'2sigma_u',@o1,
				'1pi_u',@o2,
				'3sigma_g',@o3,
				'1pi_g',@o4,
				'3sigma_u',@o5,
				'3ssigma_g',@o6
			)
		)
	),
	specie_id = (select max(id) from nepc.species where name = 'N2');

LOAD DATA LOCAL INFILE 'total'
	INTO TABLE nepc.cs
	(id,@specie,process_id,units_e,units_sigma)
	SET specie_id = (select id from nepc.species where name = @specie);
/*
	process_id = (select id from nepc.processes where name = @process);
	lhs_id = (select id from nepc.states where name = @lhs),
	rhs_id = (select id from nepc.states where name = @rhs),
*/

LOAD DATA LOCAL INFILE 'total_data'
	INTO TABLE nepc.csdata
	(id,e,sigma)
	SET cs_id = 1;

