DROP DATABASE IF EXISTS `nep3`;
CREATE DATABASE IF NOT EXISTS `nep3`;

SET default_storage_engine = INNODB;

CREATE TABLE `nep3`.`species`(
	`id` INT UNSIGNED NOT NULL auto_increment ,
	`name` VARCHAR(40) NOT NULL ,
	`tex` VARCHAR(40) NOT NULL ,
	PRIMARY KEY(`id`)
);

CREATE TABLE `nep3`.`states`(
	`id` INT UNSIGNED NOT NULL AUTO_INCREMENT ,
	`specie_id` INT UNSIGNED NOT NULL ,
	`term` VARCHAR(40) NOT NULL ,
	`configuration` JSON NOT NULL ,
	PRIMARY KEY(`id`) ,
	INDEX `SPECIE_ID`(`specie_id` ASC) ,
	CONSTRAINT `specie_id` FOREIGN KEY(`specie_id`) 
		REFERENCES `nep3`.`species`(`id`) 
		ON DELETE RESTRICT ON UPDATE CASCADE
);

/***************/
/** Load data **/
/***************/
LOAD DATA LOCAL INFILE 'species.txt' 
	INTO TABLE nep3.species;

LOAD DATA LOCAL INFILE 'states.tex'    
	INTO TABLE nep3.states
	FIELDS TERMINATED BY '&'
	LINES TERMINATED BY '\\'
	IGNORE 3 LINES
	(id,@o1,@o2,@o3,@o4,@o5,@o6,term)
	SET configuration = JSON_OBJECT(
		JSON_QUOTE('2\\ce{\\sigma_u}'),@o1,
		'1\ce{\pi_u}',@o2,
		'3\ce{\sigma_g}',@o3,
		'1\ce{\pi_g}',@o4,
		'3\ce{\sigma_u}',@o5,
		'3\ce{\sigma_g}',@o6
	),
	specie_id = (select max(id) from nep3.species where name = 'N2');
