'''
Project 	::	Voicemail
Author 		:: 	AH40222
Date 		:: 	29-04-2022
description :: 	[1]: This sql statemetns we need to run once we configure the application ! 
				
				[2]: The trigger will invokes imideatly after each new record added or update actions performs on top 
				the voicemail_transaction table then the db triggers it self take care to mantain the history
				to clones that record on top the voicemail_transaction_archive, that is how the trigges helps us.

				[3]: The defined event scheduler db job will take care and help us to push 
				the records in to overdue once the voicemail records completes 24 hrs after receving !

'''

show events;
show triggers;
DROP TRIGGER IF EXISTS srchiveDB.voicemail_transaction_after_ins_trg;
DROP TRIGGER IF EXISTS srchiveDB.voicemail_transaction_after_upt_trg;

DELIMITER $$
DROP TRIGGER IF EXISTS srchiveDB.voicemail_transaction_after_ins_trg$$
USE `srchiveDB`$$
	CREATE DEFINER = CURRENT_USER TRIGGER `srchiveDB`.`voicemail_transaction_after_ins_trg` AFTER INSERT ON voicemail_transaction FOR EACH ROW
    BEGIN
		SET @lst_id=(SELECT MAX( vm_id ) FROM voicemail_transaction);
		IF @lst_id!=0 THEN
			INSERT INTO voicemail_transaction_archive(vm_id, vm_uuid, vm_name, vm_member_name, vm_audio_url, vm_system_state, vm_review_state, vm_timestamp, vm_active_status, vm_ner, vm_call_reason, vm_callback_no, vm_extension_id, vm_transcript_dtls, vm_normalized_dtls, vm_reviewer_name, vm_review_start_date, vm_review_end_date, vm_reviewer_comments, vm_call_duration, vm_member_called_back, vm_callback_no_reachable, vm_is_overdue) 
			SELECT vm_id, vm_uuid, vm_name, vm_member_name, vm_audio_url, vm_system_state, vm_review_state, vm_timestamp, vm_active_status, vm_ner, vm_call_reason, vm_callback_no, vm_extension_id, vm_transcript_dtls, vm_normalized_dtls, vm_reviewer_name, vm_review_start_date, vm_review_end_date, vm_reviewer_comments, vm_call_duration, vm_member_called_back, vm_callback_no_reachable, vm_is_overdue
			FROM voicemail_transaction WHERE vm_uuid IS NOT NULL AND vm_id = new.vm_id;
		END IF;
    END; $$
DELIMITER ;

DELIMITER $$
DROP TRIGGER IF EXISTS srchiveDB.voicemail_transaction_after_upt_trg$$
USE `srchiveDB`$$
	CREATE DEFINER = CURRENT_USER TRIGGER `srchiveDB`.`voicemail_transaction_after_upt_trg` AFTER UPDATE ON voicemail_transaction FOR EACH ROW
    BEGIN
		INSERT INTO voicemail_transaction_archive(vm_id, vm_uuid, vm_name, vm_member_name, vm_audio_url, vm_system_state, vm_review_state, vm_timestamp, vm_active_status, vm_ner, vm_call_reason, vm_callback_no, vm_extension_id, vm_transcript_dtls, vm_normalized_dtls, vm_reviewer_name, vm_review_start_date, vm_review_end_date, vm_reviewer_comments, vm_call_duration, vm_member_called_back, vm_callback_no_reachable, vm_is_overdue) 
        SELECT vm_id, vm_uuid, vm_name, vm_member_name, vm_audio_url, vm_system_state, vm_review_state, vm_timestamp, vm_active_status, vm_ner, vm_call_reason, vm_callback_no, vm_extension_id, vm_transcript_dtls, vm_normalized_dtls, vm_reviewer_name, vm_review_start_date, vm_review_end_date, vm_reviewer_comments, vm_call_duration, vm_member_called_back, vm_callback_no_reachable, vm_is_overdue
        FROM voicemail_transaction WHERE vm_uuid IS NOT NULL AND vm_id = new.vm_id;
	END; $$
DELIMITER ;


''' event change pending state to overdue '''

CREATE EVENT set_vm_review_state ON SCHEDULE EVERY '90' SECOND STARTS '2022-06-13'
DO 
	UPDATE voicemail_transaction SET vm_review_state = "Overdue", vm_is_overdue = 1 WHERE vm_timestamp <= DATE_SUB(CONVERT_TZ(now(), 'UTC', 'America/New_York'), INTERVAL 24 HOUR) AND LOWER(vm_review_state) LIKE "%Pending%";


CREATE EVENT set_vm_inprogress_state ON SCHEDULE EVERY '165' SECOND STARTS '2022-06-13'
DO 
	UPDATE voicemail_transaction SET vm_is_overdue = 1 WHERE vm_timestamp <= DATE_SUB(CONVERT_TZ(now(), 'UTC', 'America/New_York'), INTERVAL 24 HOUR) AND LOWER(vm_review_state) LIKE "%InProgress%";
    
    

''' insert voicemail boxs '''
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('FDL EGR SPANISH ALL',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('FDL SENIOR VM CENTRAL EGR PDP FI',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('FDL SENIOR VM CENTRAL EGR MAPD FI',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('FDL EGR CENTRAL MAPD',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('FDL EGR CENTRAL PDP',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('FDL EGR WLP RETIREE DEDICATED',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('FDL EGR 1ST ENERGY DEDICATED',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('FDL SENIOR EGR EAST MAPD FI',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('FDL EGR EAST MAPD',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('FDL EGR CITY OF ALBANY DEDICATED',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('SHBP',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('SHBP FI',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('FDL SENIOR EGR WEST PDP FI',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('FDL SENIOR EGR WEST PDP CS',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('FDL SENIOR VM NV PPO EGR FI',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('FDL SENIOR VM GA HMO EGR FI',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('FDL EGR WEST MAPD',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('FDL SENIOR LAPRA DEDICATED',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('University of CA - Member',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('University of CA - Transfers',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('Calpers EGR CS',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('GBD Shared FI',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('GBD Shared Post',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('ITDR FI',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('ITDR Member',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('MPI FI',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('MPI Post Enrollment',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('TRB FI',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('TRB Post Enrollment',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('PERA',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('PERA FI',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('State of New Hampshire',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('LAUSD',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('LAUSD FI',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('University of Chicago',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('University of Chicago FI',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('MAPD/Duals East Coast',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('MAPD/Duals Central',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('MAPD/Duals West',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('TN Duals',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('MA Spanish',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('AMV Spanish',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('MMP Member English',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('MMP Spanish',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('MMP Provider',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('AMV English',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('MEABT FI',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('INTEL CORPORATION GRS FI',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('LEVEL CARE HEALTH GRS FI',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('NY Emblem FI ( informational only )',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('Arcadia University',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('AFL-CIO Mutual Benefit Fund',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('Southern Company',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('Intel Box 2',now(),1);
insert into voicemail_box (vmb_name,vmb_timestamp,vmb_status)values('Labor First',now(),1);



''' insert voicemail features '''
insert into voicemail_features (vmf_name,vmf_timestamp,vmf_status)values('Access to Care','now()',1);
insert into voicemail_features (vmf_name,vmf_timestamp,vmf_status)values('Authorization','now()',1);
insert into voicemail_features (vmf_name,vmf_timestamp,vmf_status)values('Benefits','now()',1);
insert into voicemail_features (vmf_name,vmf_timestamp,vmf_status)values('Claim','now()',1);
insert into voicemail_features (vmf_name,vmf_timestamp,vmf_status)values('EE Benefits','now()',1);
insert into voicemail_features (vmf_name,vmf_timestamp,vmf_status)values('Grievance and/or Appeal','now()',1);
insert into voicemail_features (vmf_name,vmf_timestamp,vmf_status)values('ID Card','now()',1);
insert into voicemail_features (vmf_name,vmf_timestamp,vmf_status)values('Membership/Enrollment','now()',1);
insert into voicemail_features (vmf_name,vmf_timestamp,vmf_status)values('Monthly Premium','now()',1);
insert into voicemail_features (vmf_name,vmf_timestamp,vmf_status)values('Need Case Management','now()',1);
insert into voicemail_features (vmf_name,vmf_timestamp,vmf_status)values('No Reason Given','now()',1);
insert into voicemail_features (vmf_name,vmf_timestamp,vmf_status)values('Nurse Line','now()',1);
insert into voicemail_features (vmf_name,vmf_timestamp,vmf_status)values('OTC','now()',1);
insert into voicemail_features (vmf_name,vmf_timestamp,vmf_status)values('Provider','now()',1);
insert into voicemail_features (vmf_name,vmf_timestamp,vmf_status)values('RX/Pharmacy','now()',1);
insert into voicemail_features (vmf_name,vmf_timestamp,vmf_status)values('Transportation','now()',1);
