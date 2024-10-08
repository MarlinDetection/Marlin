# t-shark filters by generation
ignore_problems = f'!(_ws.expert.severity == "Warning") and !(_ws.expert.severity == "Error")'
ignore_errors = ''

# LTE
lte_rar_filter = '(mac-lte.rnti-type == 2)'
lte_setup_filter = '(lte-rrc.c1 == 3 and lte-rrc.c1 == 0 and mac-lte.dlsch.lcid == 0x00)'
downlink_lte = 'mac-lte.rnti-type == 3'
identity_request_filter = "(nas_eps.nas_msg_emm_type == 0x55 and nas_eps.emm.id_type2 == 1)"
tau_reject_filter = "(nas_eps.nas_msg_emm_type == 0x4b and (nas_eps.emm.cause == 3 or nas_eps.emm.cause == 6 or nas_eps.emm.cause == 7 or nas_eps.emm.cause == 8 or nas_eps.emm.cause == 12 or nas_eps.emm.cause == 14 or nas_eps.emm.cause == 35))"
detach_request_filter = "(nas_eps.nas_msg_emm_type == 0x45 and !(nas_eps.emm.detach_type_dl == 3))"
attach_reject_filter = "(nas_eps.nas_msg_emm_type == 0x44 and (nas_eps.emm.cause == 3 or nas_eps.emm.cause == 6 or nas_eps.emm.cause == 7 or nas_eps.emm.cause == 8 or nas_eps.emm.cause == 11 or nas_eps.emm.cause == 12 or nas_eps.emm.cause == 13 or nas_eps.emm.cause == 14 or nas_eps.emm.cause == 15 or nas_eps.emm.cause == 35))"
service_reject_filter = "(nas_eps.nas_msg_emm_type == 0x4e and (nas_eps.emm.cause == 3 or nas_eps.emm.cause == 6 or nas_eps.emm.cause == 7 or nas_eps.emm.cause == 9 or nas_eps.emm.cause == 12 or nas_eps.emm.cause == 14 or nas_eps.emm.cause == 35))"

lte_separate_dict = {'RAR':                 lte_rar_filter,
                     'Connection Setup':    lte_setup_filter,
                     'Identity Request':    identity_request_filter,
                     'TAU Reject':          tau_reject_filter,
                     'Attach Reject':       attach_reject_filter,
                     'Detach Request':      detach_request_filter,
                     'Service Reject':      service_reject_filter}

imsi_exposing_filter_lte = f"({identity_request_filter} or {tau_reject_filter} or {detach_request_filter} or {attach_reject_filter} or {service_reject_filter} or {lte_rar_filter} or {lte_setup_filter})"
all_lte = f"({lte_rar_filter} or {lte_setup_filter} or {imsi_exposing_filter_lte})"


log_lte_dict = {'Received Identity Request':    'Identity Request',
                'Received ConnectionReject':    'Attach Reject',
                'Received Attach Reject':       'Attach Reject'}

# UMTS
downlink_umts = 'rrc.message == 5'
identity_request_umts = '(gsm_a.dtap.msg_mm_type == 0x18 and gsm_a.dtap.type_of_identity == 1)'
authentication_reject_umts = '(gsm_a.dtap.msg_mm_type == 0x11)'
location_updating_reject_umts = '(gsm_a.dtap.msg_mm_type == 0x04 and (gsm_a.dtap.rej_cause == 2 or gsm_a.dtap.rej_cause == 3 or gsm_a.dtap.rej_cause == 6 or gsm_a.dtap.rej_cause == 11 or gsm_a.dtap.rej_cause == 12))'
cm_service_reject_umts = '(gsm_a.dtap.msg_mm_type == 0x22 and (gsm_a.dtap.rej_cause == 4 or gsm_a.dtap.rej_cause == 6))'
attach_reject_umts = '(gsm_a.dtap.msg_mm_type == 0x04 and (gsm_a.gm.gmm.cause == 3 or gsm_a.gm.gmm.cause == 6 or gsm_a.gm.gmm.cause == 7 or gsm_a.gm.gmm.cause == 8 or gsm_a.gm.gmm.cause == 11 or gsm_a.gm.gmm.cause == 12 or gsm_a.gm.gmm.cause == 13 or gsm_a.gm.gmm.cause == 14 or gsm_a.gm.gmm.cause == 15))'
detach_request_umts = '(gsm_a.dtap.msg_mm_type == 0x05 and gsm_a.gm.gmm.type_of_detach == 0x02 and (gsm_a.gm.gmm.cause == 2 or gsm_a.gm.gmm.cause == 3 or gsm_a.gm.gmm.cause == 6 or gsm_a.gm.gmm.cause == 8 or gsm_a.gm.gmm.cause == 11 or gsm_a.gm.gmm.cause == 12 or gsm_a.gm.gmm.cause == 13 or gsm_a.gm.gmm.cause == 14 or gsm_a.gm.gmm.cause == 15))'
rau_reject_umts = '(gsm_a.dtap.msg_gmm_type == 0x0b and (gsm_a.gm.gmm.cause == 3 or gsm_a.gm.gmm.cause == 6 or gsm_a.gm.gmm.cause == 7 or gsm_a.gm.gmm.cause == 9 or gsm_a.gm.gmm.cause == 11 or gsm_a.gm.gmm.cause == 12 or gsm_a.gm.gmm.cause == 14))'
auth_cipher_reject_umts = '(gsm_a.dtap.msg_mm_type == 0x14)'
service_reject_umts = '(gsm_a.dtap.msg_mm_type == 0x0e and (gsm_a.gm.gmm.cause == 3 or gsm_a.gm.gmm.cause == 6 or gsm_a.gm.gmm.cause == 7 or gsm_a.gm.gmm.cause == 9 or gsm_a.gm.gmm.cause == 11 or gsm_a.gm.gmm.cause == 12))'

umts_separate_dict = {'Identity Request':               identity_request_umts,
                      'Authentication Reject':          authentication_reject_umts,
                      'Location Updating Reject':       location_updating_reject_umts,
                      'CM Service Reject':              cm_service_reject_umts,
                      'Attach Reject':                  attach_reject_umts,
                      'Detach Request':                 detach_request_umts,
                      'RAU Reject':                     rau_reject_umts,
                      'Authentication Cipher Reject':   auth_cipher_reject_umts,
                      'Service Reject':                 service_reject_umts}

imsi_exposing_filter_umts = f"({identity_request_umts} or {authentication_reject_umts} or {location_updating_reject_umts} or {cm_service_reject_umts} or {attach_reject_umts} or {detach_request_umts} or {rau_reject_umts} or {auth_cipher_reject_umts} or {service_reject_umts}) and {downlink_umts} and {ignore_problems}"

# GSM
# downlink_gsm = '(gsmtap.chan_type == 6 or gsmtap.chan_type == 7 or gsmtap.chan_type == 8)'
downlink_gsm = '(gsmtap.uplink == 0 and gsm_a.dtap)'
gsm_immediate_assignment = "(gsm_a.dtap.msg_rr_type == 0x3f and gsm_a.rr.timeslot == 1)"
identity_request_gsm = '(gsm_a.dtap.msg_mm_type == 0x18 and gsm_a.dtap.type_of_identity == 1)'
authentication_reject_gsm = '(gsm_a.dtap.msg_mm_type == 0x11)'
location_updating_reject_gsm = '(gsm_a.dtap.msg_mm_type == 0x04 and (gsm_a.dtap.rej_cause == 2 or gsm_a.dtap.rej_cause == 3 or gsm_a.dtap.rej_cause == 6 or gsm_a.dtap.rej_cause == 11 or gsm_a.dtap.rej_cause == 12 or gsm_a.dtap.rej_cause == 13))'
cm_service_reject_gsm = '(gsm_a.dtap.msg_mm_type == 0x22 and (gsm_a.dtap.rej_cause == 4 or gsm_a.dtap.rej_cause == 6))'

gsm_separate_dict = {'Identity Request':               identity_request_gsm,
                      'Authentication Reject':          authentication_reject_gsm,
                      'Location Updating Reject':       location_updating_reject_gsm,
                      'CM Service Reject':              cm_service_reject_gsm}

imsi_exposing_filter_gsm = f"({identity_request_gsm} or {authentication_reject_gsm} or {location_updating_reject_gsm} or {cm_service_reject_gsm}) and {downlink_gsm} and {ignore_problems}"

# Dictionaries to hold data
downlink_filter_dict = {'5G NSA': downlink_lte,
                        'LTE': downlink_lte,
                        'UMTS': downlink_umts,
                        'GSM': downlink_gsm}
imsi_exposing_filter_dict = {'5G NSA': imsi_exposing_filter_lte,
                             'LTE': imsi_exposing_filter_lte,
                             'UMTS': imsi_exposing_filter_umts,
                             'GSM': imsi_exposing_filter_gsm}

# User encapsulation settings necessary to read LTE frames
my_parameters = ['-o', 'uat:user_dlts:"User 0 (DLT=147)","mac-lte-framed","0","","0",""',
                 '-o', 'uat:user_dlts:"User 1 (DLT=148)","nas-eps","0","","0",""',
                 '-o', 'uat:user_dlts:"User 2 (DLT=149)","udp","0","","0",""',
                 '-o', 'uat:user_dlts:"User 3 (DLT=150)","s1ap","0","","0",""']

# Convert a given EARFCN to an exact frequency returned as an integer
def convert_earfcn_to_freq(earfcn):
    
    # F_downlink = F_DL_Low + 0.1*(N_DL - N_DL_offset)
    
    # Mapping from N_DL_offset to F_DL_Low
    DL_offset_dict = {0:  2110.0,
                    600:  1930.0,
                    1200: 1805.0,
                    1950: 2110.0,
                    2400: 869.0,
                    2650: 875.0,
                    2750: 2620.0,
                    3450: 925.0,
                    3800: 1844.9,
                    4150: 2110.0,
                    4750: 1475.9,
                    5000: 728.0,
                    5180: 746.0,
                    5280: 758.0,
                    5730: 734.0,
                    5850: 860.0,
                    6000: 875.0,
                    6150: 791.0,
                    6450: 1495.9,
                    6600: 3510.0,
                    7700: 1525.0,
                    8040: 1930.0,
                    8690: 859.0,
                    9040: 852.0,
                    9210: 758.0,
                    9660: 717.0,
                    9770: 2350.0,
                    9870: 462.5,
                    9920: 1452.0,
                    36000: 1900.0,
                    36200: 2010.0,
                    36350: 1850.0,
                    36950: 1930.0,
                    37550: 1910.0,
                    37750: 2570.0,
                    38250: 1880.0,
                    38650: 2300.0,
                    39650: 2496.0,
                    41590: 3400.0,
                    43590: 3600.0,
                    45590: 703.0,
                    46590: 1447.0,
                    46790: 5150.0,
                    54540: 5855.0,
                    55240: 3550.0,
                    56740: 3550.0,
                    58240: 1432.0,
                    59090: 1427.0,
                    59140: 3300.0,
                    60140: 2483.5,
                    65536: 2110.0,
                    66436: 2110.0,
                    67336: 738.0,
                    67536: 753.0,
                    67836: 2570.0,
                    68336: 1995.0,
                    68586: 617.0,
                    68936: 461.0,
                    68986: 460.0,
                    69036: 1475.0,
                    69466: 1432.0,
                    70316: 1427.0,
                    70366: 728.0,
                    70546: 420.0,
                    70596: 422.0}

    # Calculate N_DL_offset from EARFCN
    earfcn = int(earfcn)
    N_DL_Offset = 0
    for key in DL_offset_dict:
        if (key <= earfcn) and (key > N_DL_Offset):
            N_DL_Offset = key

    # Calculate F_DL_Low from N_DL_offset
    F_DL_Low = DL_offset_dict[N_DL_Offset]
    
    F_downlink = int((F_DL_Low + 0.1 * (earfcn - N_DL_Offset)) * 1000000)
    # print(f"Downlink Frequency: {F_downlink}")
    return F_downlink