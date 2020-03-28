# Database

Here are the 5 databases:
1. diff_records_allruns
2. diff_records_outofrange
3. diff_records_reviewed
4. diff_records_normal
5. diff_records_abnormal


Contents:
1. diff_records_allruns
    a. when a technician runs a specimen, regardless of its outcome, it goes to this database.
    b. includes diff_records_outofrange.
2. diff_records_outofrange
    a. when a technician runs a specimen, but the result is out of range, it goes to this database.
3. diff_records_reviewed
    a. when a doctor comments or reviews an "out of range record" from diff_records_outofrange,
        regardless if its normal or not, it goes to this database.
    b. includes both diff_records_normal and diff_records_normal databases.
4. diff_records_normal
    a. when a doctor comments or reviews an "out of range record" from diff_records_outofrange,
        and it is "normal", it goes to this database.
    b. when a technician runs a specimen, but the result is "normal", it goes to this database.
5. diff_records_abnormal
    a. when a doctor comments or reviews an "out of range record" from diff_records_outofrange,
        and it is "abnormal", it goes to this database.


Access:
1. Medical Technician can view:
    a. diff_records_allruns
    b. diff_records_outofrange
2. Doctor can view:
    a. diff_records_outofrange
    b. diff_records_reviewed

