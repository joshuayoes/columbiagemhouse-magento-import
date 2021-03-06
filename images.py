from typing import Dict

BROKEN_URLS = [
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/8/9822-34lp-1r_2.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/8/9858-35f-1_9.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/s/t/stk-015-grp_1_4.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/0/3/031-00101-1t2r00q_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/h/4/h415-09514-a1_6-57_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/1/1151-182-1w_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/7/9730-232-1w_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/7/9731-182-1w_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/7/9733-125-1r_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/3/9383-590-1s_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/3/9385-590-1s_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/3/9386-44-1s_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/7/9745-157-1s_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/7/9747-37-1s_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/3/9382-45-1w_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/3/9387-592-1s_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/b/b/bbs-001-grp_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/b/b/bbs-003-grp_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/b/b/bbs-006-grp_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/b/b/bbs-007-grp_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/b/b/bbs-008-grp_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/b/b/bbs-009-grp_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/0/4/045-12130-1_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/8/9822-34ly-1w.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/8/9824-34lb-1w.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/8/9828-34lb-1w.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/8/9830-34mb-1r.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/j/0/j034-01022-1_66-68.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/j/0/j034-01025-1_9-17.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/j/0/j034-01025-1_15-82.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/j/0/j034-01025-1_4-12.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/j/0/j034-01025-1_1-99.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/j/0/j034-01025-1_4-36.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/j/0/j034-01025-1_3-36.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/j/0/j034-01025-1_8-38.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/0/8/083-01035-1_s.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/m/t/mt-001-grp-c.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/i/d/id-001-grp_c.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/w/y/wy-001_grp-c.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/s/a/sample_summer_social_7_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/s/a/sample_summer_social_7_1_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/s/a/samplesummer_ad_2.png",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/s/a/samplesummer_ad_2_1.png",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/9/9917-000-1_2.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/9/9917-000-1w_3.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/9/9901-000-1w.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/9/9901-000-1w_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/9/9929-34mb-1w.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/9/9923-000-1w.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/9/9923-000-1w_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/9/9923-000-1w_2.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/0/10025-261-1_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/w/i/winter2017_sample_2.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/w/i/winter2017_sample_3_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/c/c/ccc_17_winter_sample_3.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/c/c/ccc_17_winter_sample_3_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/2/8/280-09180-1_group.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/l/4/l4039-594-1w.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/s/a/sampleh001_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/s/a/sampleh001_2.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/s/a/sampleh003_3.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/s/a/sampleh001_4.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/2/121-01030-1_1_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/2/121-01030-1_1_1_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/2/121-01030-1_1_1_2.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/2/121-01030-1_1_1_3.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/6/0/60-1035-aa.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/6/4/64-10190-1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/0/10025-101-1s_a.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/0/10025-157-1s_a.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/0/10025-180-1s_a.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/0/10025-200-1s_a.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/0/10025-45-2s_a.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/0/10025-50-1s_a.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/0/10025-640-1s_a.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/0/10025-80-1s_a.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/0/10025-99-1s_a.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/0/10025-45-2s_a_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/0/10025-130-1s_a.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/0/10025-125-1s_a.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/c/i/citrine_1_3.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/e/1/e146-00101-2t3_2-18_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/e/1/e146-01082-1_2-31_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/4/3/432-709010-aaa_9-10bar.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/4/3/432-mabe9510-aa.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/9/9922-32-1w.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/8/9898-34lb-1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/4/4/44-1060-1_2.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/9/9910m-000-1_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/9/9949m-000-1w.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/9/9927-000-1w_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/9/9920-000-1w.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/9/9901-000-1w_3.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/7/9700-80-1ys_1_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/5/9567-50-1ys_1_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/7/9774-520-1s_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/s/9/s9898-280-1w_2.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/s/t/stk-015-grp_1_3.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/4/9442-32fb-1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/5/6/5635m-45-1w.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/5/9565-185-1ys_1_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/9/9968-150-1w.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/9/9969d-594-1w.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/9/9964-260-1w.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/2/0/2064m-180-1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/2/0/2065m-181-1w.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/9/9962-260-1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/n/2/n2063-260-1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/0/10530-70-1wb.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/0/10260-595-1b.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/0/10165-594-1wb.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/0/10190-520-1wb.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/1/11050-170-1wb.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/8/9879-640-1_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/7/9778-371-1ys.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/2/3/230-1070-fcy.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/1/1115-200-1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/1/1118-150-1w_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/8/9864-80-1w.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/8/18k7715-35-1e.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/7/3/7308-170-2wd.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/7/3/7354-34-1b.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/8/18k7941-29-2b.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/7/1/7154-200-1ysc.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/7/1/7156-200-1rsc.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/7/1/7152-260-1rd.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/l/n/ln117-p593-g_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/s/e/seneck10-p_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/2/1239-p-590-g_2.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/s/e/seneck8-p_2.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/s/e/seneck3-p_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/3/5/35-12122-fc-yellow.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/3/5/35-302-fc-ltylwblue.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/5/157-1450-1a.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/5/157-106-1a.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/5/157-10460-1a.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/3/5/35-304-fc_denim.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/h/0/h056-304-1_dark.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/n/8/n807-601-999_a.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/6/0/60-304-c.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/6/1/610-13551-1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/n/1/n1257-125-1r_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/n/8/n801-601-260.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/n/1/n1261-99-157-1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/0/106-13410-1_light.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/s/t/stk-001-grp_1_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/n/1/n1264-630-590-1w.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/n/1/n1263-366-170-1r_v2_3.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/7/173-1030-1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/7/173-1050-1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/6/5/65-107-1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/e/0/e034-11957-1_steel-teal.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/e/0/e034-11940-1.jpg    ",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/e/0/e034-11960-1_steel-blue.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/0/1/016-01050-aaa_0-58_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/6/5/65-322-1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/3/7/371-91xx-rnd-2.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/6/160-9210-1_1_2.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/0/9/090-9210-aa_1_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/7/172-9210-1_1_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/7/171-9210-1_1_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/2/120-9210-1_1_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/4/1/41-12130-1_purple.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/4/0/405-09501-playofc_20-13.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/4/0/405-1440-1y.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/8/98-crv01-cat_b1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/8/98-crv01-seal_b1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/8/98-crv01-starfish_a1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/8/98-crv01-turtle_a1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/8/98-crv01-seahorse_b1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/8/98-crv01-flower-5_c1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/l/a/large-green-turtle_d1_1_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/j/0/j035-240-b_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/j/0/j035-240-b_1_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/j/0/j035-240-b_1_1_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/j/0/j035-240-b_1_2.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/l/a/large-purple-tort-on-crystal_g1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/s/m/small-purple-turtle-on-crystal_c1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/s/m/small-purple-tort_e1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/s/m/small-purple-tort-on-crystal_c1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/0/3/034-yogo-15-20.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/2/1253-520-1r_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/2/1251-000-1w_a.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/2/9257-260-1w.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/9/9957m-34lp-1w_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/9/9959m-34lm-1w_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/8/9808-200-1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/3/93-112-0.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/j/0/j034-506-1_0-45_stone2.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/5/157-303-1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/1/0/108-5115-1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/2/3/230-1670-1_3-38.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/5/0/503-9551-2__95_.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/5/6/565-8991-1_3.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/5/6/565-8991-1_3_1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/6/2/620-9525x18-1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/e/0/e034-705-1_group-2.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/e/0/e034-11940-1.jpg",
    "https://columbiagemhouse.com/media/catalog/product/cache/1/image/400x400/9df78eab33525d08d6e5fb8d27136e95/9/5/9571-80-1ys_1_1.jpg",
]

BROKEN_URL_MAP: Dict[str, bool] = {}
for url in BROKEN_URLS:
    BROKEN_URL_MAP[url] = True

def is_url_broken(url: str):
    try:
        return BROKEN_URL_MAP[url]
    except KeyError:
        return False
