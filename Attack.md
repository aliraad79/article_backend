# Attack

When large number of users want to down-vote/up-vote a particular article we can use statical analysis to find this anomalis and don't affect this votes for 24 hours. for this purpose for every vote we calculate z_score for that vote and if it is not a normal vote for that document and if it is not a normal distributed vote we disable it for further operation review.