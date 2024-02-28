#!/usr/bin/env python
# coding: utf-8

# Berikut adalah script untuk mengubah pdf lampiran profil kesehatan Jawa Barat jadi csv
# Caveat: script setiap tahun berbeda karena halaman dan kerangka tabel berbeda-beda setiap tahunnya. Sehingga tidak dapat dilakukan automasi.
# Feel free to give me any suggestions
# 
# Cara run </br>
# python export_data_to_csv.py index_halaman_start index_halaman_end
# 
# Misal </br>
# python export_data_to_csv.py 0 100

# In[1]:


# import library
import tabula
import camelot
import pandas as pd
import datetime as dt
import sys

pd.options.display.max_columns = None


# ## Scraping Data

# In[159]:


# Tenaga Puskemas

df = tabula.read_pdf("2022.pdf", pages="56")[0]
df = df.iloc[:,1:]
df.rename(columns={'Jenis Tenaga Kesehatan': "Jenis Tenaga", "Jumlah Tenaga Kesehatan" : "Jumlah Tenaga"}, inplace = True)
df['Jumlah Tenaga'] = df['Jumlah Tenaga'].astype(str)
df['Jumlah Tenaga'] = df['Jumlah Tenaga'].str.replace(".", "")

df['Jumlah Tenaga'] = df['Jumlah Tenaga'].astype(int)
df['tahun'] = "2022"
df['unit_kerja'] = "puskesmas"


# In[53]:


# Tenaga Rumah Sakit
df = tabula.read_pdf("2022.pdf", pages="60")[0]
df.dropna(inplace=True)
df.rename(columns={'Jenis Tenaga Kesehatan': "Jenis Tenaga", "Jumlah Tenaga Kesehatan" : "Jumlah Tenaga"}, inplace = True)
df['Jumlah Tenaga'] = df['Jumlah Tenaga'].astype(str)
df['Jumlah Tenaga'] = df['Jumlah Tenaga'].str.replace(".", "")

df['Jumlah Tenaga'] = df['Jumlah Tenaga'].astype(int)
df['tahun'] = "2022"
df['unit_kerja'] = "rumah sakit"


# In[52]:


## Rekapitulasi Rasio Tenaga Kesehatan /100.000
df = tabula.read_pdf("2022.pdf", pages="61")[1]
df = df.iloc[3:,1:3]
df.set_axis(["jenis_tenaga","Ratio/100.000 Penduduk"], axis=1, inplace=True)
df['Ratio/100.000 Penduduk'] = df['Ratio/100.000 Penduduk'].str.replace(',','.')
df['Ratio/100.000 Penduduk'] = df['Ratio/100.000 Penduduk'].astype(float)
df.replace("Tenaga\rTeknisKefarmasian", "Tenaga Teknis Kefarmasian", inplace=True)

df2 = tabula.read_pdf("2022.pdf", pages="62")[0]
header_value = list(df2.columns)
df2 = df2.append(pd.Series(header_value, index=df2.columns), ignore_index=True)
df2 = df2.iloc[:,1:3]
df2.set_axis(["jenis_tenaga","Ratio/100.000 Penduduk"], axis=1, inplace=True)
df2['Ratio/100.000 Penduduk'] = df2['Ratio/100.000 Penduduk'].str.replace(',','.')
df2['Ratio/100.000 Penduduk'] = df2['Ratio/100.000 Penduduk'].astype(float)
df2

df = pd.concat([df,df2], ignore_index = True)
df['tahun'] = "2022"


# In[174]:


## Jumlah Fasilitas Kesehatan Menurut Kepemilikan 
### Data ini dicek secara manual pada setiap laporan kesehatan per kab/kota 2022

data = {
    'Kabupaten/Kota': ['KABUPATEN BOGOR', 'KABUPATEN SUKABUMI', 'KABUPATEN CIANJUR', 'KABUPATEN BANDUNG', 'KABUPATEN GARUT',
                            'KABUPATEN TASIKMALAYA', 'KABUPATEN CIAMIS', 'KABUPATEN KUNINGAN', 'KABUPATEN CIREBON',
                            'KABUPATEN MAJALENGKA', 'KABUPATEN SUMEDANG', 'KABUPATEN INDRAMAYU', 'KABUPATEN SUBANG',
                            'KABUPATEN PURWAKARTA', 'KABUPATEN KARAWANG', 'KABUPATEN BEKASI', 'KABUPATEN BANDUNG BARAT',
                            'KABUPATEN PANGANDARAN', 'KOTA BOGOR', 'KOTA SUKABUMI', 'KOTA BANDUNG', 'KOTA CIREBON',
                            'KOTA BEKASI', 'KOTA DEPOK', 'KOTA CIMAHI', 'KOTA TASIKMALAYA', 'KOTA BANJAR'],
    'Jumlah': [298, 31, 0, 13, 6, 10, 8, 63, 251, 51, 27, 77, 13, 0, 276, 66, 0, 3, 75, 40, 0, 45, 66, 131, 69, 27, 16]
}

df = pd.DataFrame(data)
df['tahun'] = "2022"


# In[196]:


### PELAYANAN KESEHATAN GIGI DAN MULUT MENURUT KECAMATAN DAN PUSKESMAS

tables = camelot.read_pdf("2022.pdf", flavor='stream', pages='288')

df = tables[0].df
df.columns = df.iloc[5]

df = df.iloc[6:,[1,3,5,9,11,13,15] ]
df.reset_index(drop=True, inplace=True)
df.iloc[26,0] = "Jawa Barat"
df.set_axis(["Kabupaten/Kota", "Jumlah Tumpatan Gigi Tetap", "Pencabutan Gigi Tetap", "Rasio Pencabutan", "Jumlah Kasus Gigi", "Jumlah Kasus dirujuk", "% Rasio Dirujuk"], axis=1, inplace=True)
df = df.replace('', '0')
df = df.replace('-', '0')
for col in ['Rasio Pencabutan', '% Rasio Dirujuk']:
    df[col] = df[col].str.replace(',', '.').astype(float)

for col in ['Jumlah Tumpatan Gigi Tetap', 'Pencabutan Gigi Tetap', 'Jumlah Kasus Gigi', 'Jumlah Kasus dirujuk']:
    df[col] = df[col].str.replace('.', '').astype(int)
df['tahun'] = "2022"
df['unit_kerja'] = "puskesmas"


# In[180]:


## PELAYANAN KESEHATAN GIGI DAN MULUT PADA ANAK SD DAN SETINGKAT MENURUT JENIS KELAMIN, KECAMATAN, DAN PUSKESMAS

tables = camelot.read_pdf("2022.pdf", flavor='stream', pages='289')

df = tables[0].df
# df.columns = df.iloc[7]

df = df.iloc[9:, [1, 2, 4, 5] + list(range(7, df.shape[1])) ]
# ### Replace #### Value
df.iloc[df[1] == 'Kabupaten Sumedang', 1:] = 0

df.reset_index(drop=True, inplace=True)
df = df.rename_axis(None, axis=1)
df.iloc[27,0] = "Jawa Barat"
df.set_axis(['Kabupaten/Kota', 'jumlah_SD/MI','jumlah_SD/MI_SG_Massal','%jumlah_SD/MI_SG_Massal',
             'jumlah_SD/MI_LG','%jumlah_SD/MI_LG',
            'jumlah_murid_SD/MI_L', 'jumlah_murid_SD/MI_P', 'jumlah_murid_SD/MI_LP',
            'jumlah_murid_SD/MI_L_Diperiksa','%jumlah_murid_SD/MI_L_Diperiksa','jumlah_murid_SD/MI_P_Diperiksa','%jumlah_murid_SD/MI_P_Diperiksa', 'jumlah_murid_SD/MI_LP_Diperiksa','%jumlah_murid_SD/MI_LP_Diperiksa',
            'jumlah_murid_SD/MI_L_PR','jumlah_murid_SD/MI_P_PR','jumlah_murid_SD/MI_LP_PR',
            'jumlah_murid_SD/MI_L_MP','%jumlah_murid_SD/MI_L_MP','jumlah_murid_SD/MI_P_MP','%jumlah_murid_SD/MI_P_MP','jumlah_murid_SD/MI_LP_MP','%jumlah_murid_SD/MI_LP_MP'], axis=1, inplace=True)
df = df.replace('', '0')
df = df.replace('-', '0')

## Replace ####
for col in df.columns:
    df.loc[df[col].astype(str).str.contains('#'), col] = 0

for col in df.columns[df.columns.str.contains('%')]:
    df[col] = df[col].str.replace(',', '.').astype(float)

for col in df.columns[~(df.columns.str.contains('%') | (df.columns == 'Kabupaten/Kota'))]:
    df[col] = df[col].replace('\.', '', regex=True).astype(int)

    
df = df.fillna(0)
#### Fix #### Value Before
df.loc[df["Kabupaten/Kota"] == 'Kabupaten Indramayu', "jumlah_murid_SD/MI_LP"] = df.loc[df["Kabupaten/Kota"] == 'Kabupaten Indramayu', "jumlah_murid_SD/MI_L"] + df.loc[df["Kabupaten/Kota"] == 'Kabupaten Indramayu', "jumlah_murid_SD/MI_P"]
df.loc[df["Kabupaten/Kota"] == 'Kabupaten Indramayu', "%jumlah_murid_SD/MI_LP_Diperiksa"] = round(df.loc[df["Kabupaten/Kota"] == 'Kabupaten Indramayu', "jumlah_murid_SD/MI_LP_Diperiksa"] / df.loc[df["Kabupaten/Kota"] == 'Kabupaten Indramayu', "jumlah_murid_SD/MI_LP"],2)
df.at[27, 'jumlah_murid_SD/MI_L'] = df.iloc[: 26]['jumlah_murid_SD/MI_L'].sum()
df.at[27, 'jumlah_murid_SD/MI_P'] = df.iloc[: 26]['jumlah_murid_SD/MI_P'].sum()
df.at[27, 'jumlah_murid_SD/MI_LP'] = df.iloc[: 26]['jumlah_murid_SD/MI_LP'].sum()
df.at[27, 'jumlah_murid_SD/MI_L_PR'] = df.iloc[: 26]['jumlah_murid_SD/MI_L_PR'].sum()
df.at[27, 'jumlah_murid_SD/MI_P_PR'] = df.iloc[: 26]['jumlah_murid_SD/MI_P_PR'].sum()
df.at[27, 'jumlah_murid_SD/MI_LP_PR'] = df.iloc[: 26]['jumlah_murid_SD/MI_LP_PR'].sum()
df.at[27, 'jumlah_murid_SD/MI_L_MP'] = df.iloc[: 26]['jumlah_murid_SD/MI_L_MP'].sum()
df.at[27, 'jumlah_murid_SD/MI_P_MP'] = df.iloc[: 26]['jumlah_murid_SD/MI_P_MP'].sum()
df.at[27, 'jumlah_murid_SD/MI_LP_MP'] = df.iloc[: 26]['jumlah_murid_SD/MI_LP_MP'].sum()
tahun = "2022"
df['tahun'] = tahun
df.to_csv(f"dataset/pelayanan_gigi_anaksd/{tahun}.csv", index=False)
df


# In[188]:


## Jumlah Tenaga Medis Per Kab/Kota Puskesmaas
tables = camelot.read_pdf("2022.pdf", flavor='stream', pages='238')

df = tables[1].df

df = df.iloc[10:, [1] + list(range(11, 17))]

# df = df.iloc[9: ]
df.set_axis(['Kab/Kota','jml_dg_l','jml_dg_p','jml_dg_lp','jml_dgsp_l','jml_dgsp_p','jml_dgsp_lp'], axis=1, inplace=True)
df = df.replace('', '0')
df = df.replace('-', '0')

for col in df.columns[~(df.columns.str.contains('%') | (df.columns == 'Kab/Kota'))]:
    df[col] = df[col].str.replace(',', '').astype(int)
    
df['Kab/Kota'] = df['Kab/Kota'].apply(lambda x: ''.join([i for i in x if not i.isdigit()]))


# In[189]:


## Jumlah Tenaga Medis Per Kab/Kota Puskesmaas
tables = camelot.read_pdf("2022.pdf", flavor='stream', pages='239')

df2 = tables[0].df

df2 = df2.iloc[:15, [0] + list(range(10, 16))]

df2 = df2.iloc[5: ]
df2.set_axis(['Kab/Kota','jml_dg_l','jml_dg_p','jml_dg_lp','jml_dgsp_l','jml_dgsp_p','jml_dgsp_lp'], axis=1, inplace=True)
df2 = df2.replace('', '0')
df2 = df2.replace('-', '0')

for col in df.columns[~(df2.columns.str.contains('%') | (df2.columns == 'Kab/Kota'))]:
    df2[col] = df2[col].str.replace(',', '').astype(int)
    
df2['Kab/Kota'] = df2['Kab/Kota'].apply(lambda x: ''.join([i for i in x if not i.isdigit()]))

df = pd.concat([df, df2], ignore_index=True)


# In[190]:


# Menggabungkan kolom 'jml_dg_l', 'jml_dg_p', 'jml_dgsp_l', dan 'jml_dgsp_p' menjadi satu kolom 'jumlah'
df_dg = pd.concat([
    df.loc[:,['Kab/Kota','jml_dg_l']].rename(columns={'jml_dg_l':'jumlah'}).assign(jns_kelamin='laki-laki', profesi='dokter gigi', unit_kerja='puskesmas'),
    df.loc[:,['Kab/Kota','jml_dg_p']].rename(columns={'jml_dg_p':'jumlah'}).assign(jns_kelamin='perempuan', profesi='dokter gigi', unit_kerja='puskesmas'),
    df.loc[:,['Kab/Kota','jml_dgsp_l']].rename(columns={'jml_dgsp_l':'jumlah'}).assign(jns_kelamin='laki-laki', profesi='dokter gigi spesialis', unit_kerja='puskesmas'),
    df.loc[:,['Kab/Kota','jml_dgsp_p']].rename(columns={'jml_dgsp_p':'jumlah'}).assign(jns_kelamin='perempuan', profesi='dokter gigi spesialis', unit_kerja='puskesmas')
], ignore_index=True)

# Menghapus duplikat dan mengurutkan data berdasarkan 'Kab/Kota' dan 'jns_kelamin'
df_dg_pks = df_dg.drop_duplicates().sort_values(['Kab/Kota','jns_kelamin'])


# In[191]:


## Jumlah Tenaga Medis Kab/Kota Rumah Sakit

tables = camelot.read_pdf("2022.pdf", flavor='stream', pages='239')

df = tables[0].df

df = df.iloc[:45, [0] + list(range(10, 16))]

df = df.iloc[18: ]
df.set_axis(['Kab/Kota','jml_dg_l','jml_dg_p','jml_dg_lp','jml_dgsp_l','jml_dgsp_p','jml_dgsp_lp'], axis=1, inplace=True)
df = df.replace('', '0')
df = df.replace('-', '0')

for col in df.columns[~(df.columns.str.contains('%') | (df.columns == 'Kab/Kota'))]:
    df[col] = df[col].str.replace(',', '').astype(int)

df['Kab/Kota'] = df['Kab/Kota'].apply(lambda x: ''.join([i for i in x if not i.isdigit()]))


# In[192]:


df_dg = pd.concat([
    df.loc[:,['Kab/Kota','jml_dg_l']].rename(columns={'jml_dg_l':'jumlah'}).assign(jns_kelamin='laki-laki', profesi='dokter gigi', unit_kerja='rumah sakit'),
    df.loc[:,['Kab/Kota','jml_dg_p']].rename(columns={'jml_dg_p':'jumlah'}).assign(jns_kelamin='perempuan', profesi='dokter gigi', unit_kerja='rumah sakit'),
    df.loc[:,['Kab/Kota','jml_dgsp_l']].rename(columns={'jml_dgsp_l':'jumlah'}).assign(jns_kelamin='laki-laki', profesi='dokter gigi spesialis', unit_kerja='rumah sakit'),
    df.loc[:,['Kab/Kota','jml_dgsp_p']].rename(columns={'jml_dgsp_p':'jumlah'}).assign(jns_kelamin='perempuan', profesi='dokter gigi spesialis', unit_kerja='rumah sakit')
], ignore_index=True)

# Menghapus duplikat dan mengurutkan data berdasarkan 'Kab/Kota' dan 'jns_kelamin'
df_dg_rs = df_dg.drop_duplicates().sort_values(['Kab/Kota','jns_kelamin'])


# In[193]:


# ## Klinik DIKLAT KESEHATAN
# _garut = pd.DataFrame({
#     'Kab/Kota': ['Kabupaten Garut'],
#     'jml_dg_l': [4],
#     'jml_dg_p': [7],
#     'jml_dgsp_l': [1],
#     'jml_dgsp_p': [0]
# })

# df_bekasi = pd.DataFrame({
#     'Kab/Kota': ['Kabupaten Bekasi'],
#     'jml_dg_l': [31],
#     'jml_dg_p': [139],
#     'jml_dgsp_l': [11],
#     'jml_dgsp_p': [28]
# })

# df_combined = pd.concat([df_garut, df_bekasi], ignore_index=True)

# df_dg = pd.concat([
#     df_combined.loc[:,['Kab/Kota','jml_dg_l']].rename(columns={'jml_dg_l':'jumlah'}).assign(jns_kelamin='laki-laki', profesi='dokter gigi', unit_kerja='klinik diklat kesehatan'),
#     df_combined.loc[:,['Kab/Kota','jml_dg_p']].rename(columns={'jml_dg_p':'jumlah'}).assign(jns_kelamin='perempuan', profesi='dokter gigi', unit_kerja='klinik diklat kesehatan'),
#     df_combined.loc[:,['Kab/Kota','jml_dgsp_l']].rename(columns={'jml_dgsp_l':'jumlah'}).assign(jns_kelamin='laki-laki', profesi='dokter gigi spesialis', unit_kerja='klinik diklat kesehatan'),
#     df_combined.loc[:,['Kab/Kota','jml_dgsp_p']].rename(columns={'jml_dgsp_p':'jumlah'}).assign(jns_kelamin='perempuan', profesi='dokter gigi spesialis', unit_kerja='klinik diklat kesehatan')
# ], ignore_index=True)

# # Menghapus duplikat dan mengurutkan data berdasarkan 'Kab/Kota' dan 'jns_kelamin'
# df_dg = df_dg.drop_duplicates().sort_values(['Kab/Kota','jns_kelamin'])
# df_dg


# In[194]:


## Klinik Dinas Kesehatan
data_karawang = {'Kab/Kota': 'Kabupaten Karawang',
              'jml_dg_l': 0,
              'jml_dg_p': 1,
              'jml_dgsp_l': 0,
              'jml_dgsp_p': 0}

data_purwakarta = {'Kab/Kota': 'Kota Purwakarta',
                'jml_dg_l': 0,
                'jml_dg_p': 1,
                'jml_dgsp_l': 0,
                'jml_dgsp_p': 0}

df_karawang = pd.DataFrame([data_karawang])
df_purwakarta = pd.DataFrame([data_purwakarta])

df_combined = pd.concat([df_karawang, df_purwakarta], ignore_index=True)

df_dg = pd.concat([
    df_combined.loc[:,['Kab/Kota','jml_dg_l']].rename(columns={'jml_dg_l':'jumlah'}).assign(jns_kelamin='laki-laki', profesi='dokter gigi', unit_kerja='klinik DINKES'),
    df_combined.loc[:,['Kab/Kota','jml_dg_p']].rename(columns={'jml_dg_p':'jumlah'}).assign(jns_kelamin='perempuan', profesi='dokter gigi', unit_kerja='klinik DINKES'),
    df_combined.loc[:,['Kab/Kota','jml_dgsp_l']].rename(columns={'jml_dgsp_l':'jumlah'}).assign(jns_kelamin='laki-laki', profesi='dokter gigi spesialis', unit_kerja='klinik DINKES'),
    df_combined.loc[:,['Kab/Kota','jml_dgsp_p']].rename(columns={'jml_dgsp_p':'jumlah'}).assign(jns_kelamin='perempuan', profesi='dokter gigi spesialis', unit_kerja='klinik DINKES')
], ignore_index=True)

# Menghapus duplikat dan mengurutkan data berdasarkan 'Kab/Kota' dan 'jns_kelamin'
df_dg_dk = df_dg.drop_duplicates().sort_values(['Kab/Kota','jns_kelamin'])
df_dg = pd.concat([df_dg_rs,df_dg_pks,df_dg_dk], ignore_index=True )
tahun = "2022"
df_dg['tahun'] = tahun


# In[197]:


df_dg.to_csv(f'dataset/dg_unit_kerja/{tahun}.csv', index=False)
print(f"Job Scraping pada Profil Kesehatan Jawa Barat tahun {tahun} sudah selesai")


# In[ ]:




