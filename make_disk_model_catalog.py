from collate_full_catalog import collate_catalog

history_colnames = ('halo_dvmax_zscore', 'halo_upid', 'halo_vmax_at_mpeak',
    'obs_sfr', 'sfr', 'obs_stellar_mass', 'stellar_mass',
    'mpeak_mp', 'sfh', 'sfr_mp', 'sm_mp')

mock = collate_catalog('a_1.002310', history_colnames=history_colnames)
mask = mock['stellar_mass'] > 10**9.75
mock = mock[mask]

