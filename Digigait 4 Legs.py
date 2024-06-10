# %% Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as scipy
import seaborn as sns
import xlrd
import glob
import os
import matplotlib.font_manager
from xls2xlsx import XLS2XLSX
sns.set()
# %% Check for Digigait .xlsx files, parse, translate

dg_folder_path = '/Volumes/Extreme SSD/Digigait 10-13 Test/Alex/'

dg_file_list = glob.glob(os.path.join(dg_folder_path, "*/result/INDICES_*.xls"))

for file in dg_file_list:

    xlsx_file = file + "x"  # XLSX file path

    if not os.path.exists(xlsx_file): # check if XLSX file exists already
        tempCSV = pd.read_csv(file, sep='\t')
        print(tempCSV)
        tempCSV.to_excel(file + "x")

new_dg_file_list = glob.glob(os.path.join(dg_folder_path, "*/result/INDICES_*.xlsx"))
print("New file list:")
print(new_dg_file_list)

total_indices_dataframe_list = []


# %% Iterate over each file in new_file_list

for indices_file in new_dg_file_list:
    # Read the current file
    cur_file = pd.read_excel(indices_file)

    # Drop the first column
    cur_file = cur_file.drop(cur_file.columns[0], axis=1)

    #Drop all of the unneeded columns
    columns_to_drop = ['Version Number ', ' User Name ', ' Comments ', ' FileName ']
    
    cur_file = cur_file.drop(columns=cur_file.columns[cur_file.columns.str.contains('|'.join(columns_to_drop))])

    # Drop the first row and reset the index
    cur_file = cur_file.drop([0]).reset_index(drop=True)
    
    cur_file.to_csv('/Users/alexzeng/Desktop/A/cur_file.csv')

    print(indices_file)

    # Split Identifiers
    lowercase_parts = [part.lower() for index, part in enumerate(indices_file.split('_')[0:5]) if index != 1]
    lowercase_parts[0] = lowercase_parts[0].replace('/volumes/extreme ssd/digigait 10-13 test/alex/', '')
    print("Lowercase Parts: ")
    print(lowercase_parts)

    column_list = ['Animal ID', 'Genotype', 'Sex', 'Age']

    for i, part in enumerate(lowercase_parts):
        cur_file.insert(i, column_list[i], part)

    print('current file: ')
    print(cur_file)

    # Concatenate the current file DataFrame to the list of DataFrames
    total_indices_dataframe_list.append(cur_file)

    # Test out Total Indices
    print(total_indices_dataframe_list)


# %% Concatenate INDICES Dataframe + Test1 CSV

presplit_dgdf = pd.concat(total_indices_dataframe_list, ignore_index=True)

print(presplit_dgdf)

presplit_dgdf.to_csv('/Users/alexzeng/Desktop/A/presplit_dgdf.csv')

# %% Seperate into genotype arrays

onlyWT = presplit_dgdf[(presplit_dgdf['Genotype'] == 'wt')]
onlyGrDf = presplit_dgdf[(presplit_dgdf['Animal ID'].str.startswith('gr')) & (presplit_dgdf['Genotype'] == 'hom')]
onlyTMDf = presplit_dgdf[(presplit_dgdf['Animal ID'].str.startswith('tm')) & (presplit_dgdf['Genotype'] == 'hom')]
onlyKODf = presplit_dgdf[(presplit_dgdf['Animal ID'].str.startswith('ko')) & (presplit_dgdf['Genotype'] == 'hom')]

onlyWT.loc[:, 'Genotype'] = 'WT'
onlyGrDf.loc[:, 'Genotype'] = 'G219R'
onlyTMDf.loc[:, 'Genotype'] = 'T230M'
onlyKODf.loc[:, 'Genotype'] = 'KO'

print(onlyTMDf)

# %% Printing resultantDF > CSV

resultantDF = pd.concat([onlyWT,onlyKODf, onlyGrDf, onlyTMDf], ignore_index=True)
resultantDF[' Ataxia Coefficient '] = resultantDF[' Ataxia Coefficient '].str.strip().astype(float)
resultantDF[' PawAngle '] = resultantDF[' PawAngle '].str.strip().astype(float)
print(resultantDF)

resultantDF.to_csv('/Users/alexzeng/Desktop/A/TestFinal.csv')



# %% Statistical Testing

resultantDF.to_csv('/Users/alexzeng/Desktop/A/prestatstesting.csv')

leftfore_data = resultantDF[(resultantDF[' Limb '] == ' Left Fore ')].dropna()

leftfore_anova_result = scipy.f_oneway(
    leftfore_data[leftfore_data['Genotype'] == 'G219R'][' Ataxia Coefficient '],
    leftfore_data[leftfore_data['Genotype'] == 'KO'][' Ataxia Coefficient '],
    leftfore_data[leftfore_data['Genotype'] == 'WT'][' Ataxia Coefficient '],
    leftfore_data[leftfore_data['Genotype'] == 'T230M'][' Ataxia Coefficient ']
)

print("Left Fore ANOVA p-value:", leftfore_anova_result.pvalue)

lefthind_data = resultantDF[(resultantDF[' Limb '] == ' Left Hind ')].dropna()

lefthind_anova_result = scipy.f_oneway(
    lefthind_data[lefthind_data['Genotype'] == 'G219R'][' Ataxia Coefficient '],
    lefthind_data[lefthind_data['Genotype'] == 'KO'][' Ataxia Coefficient '],
    lefthind_data[lefthind_data['Genotype'] == 'WT'][' Ataxia Coefficient '],
    lefthind_data[lefthind_data['Genotype'] == 'T230M'][' Ataxia Coefficient ']
)

print("Left Hind ANOVA p-value:", lefthind_anova_result.pvalue)

rightfore_data = resultantDF[(resultantDF[' Limb '] == ' Right Fore ')].dropna()

rightfore_anova_result = scipy.f_oneway(
    rightfore_data[rightfore_data['Genotype'] == 'G219R'][' Ataxia Coefficient '],
    rightfore_data[rightfore_data['Genotype'] == 'KO'][' Ataxia Coefficient '],
    rightfore_data[rightfore_data['Genotype'] == 'WT'][' Ataxia Coefficient '],
    rightfore_data[rightfore_data['Genotype'] == 'T230M'][' Ataxia Coefficient ']
)

print("Right Fore ANOVA p-value:", rightfore_anova_result.pvalue)

righthind_data = resultantDF[(resultantDF[' Limb '] == ' Right Hind ')].dropna()

righthind_anova_result = scipy.f_oneway(
    righthind_data[righthind_data['Genotype'] == 'G219R'][' Ataxia Coefficient '],
    righthind_data[righthind_data['Genotype'] == 'KO'][' Ataxia Coefficient '],
    righthind_data[righthind_data['Genotype'] == 'WT'][' Ataxia Coefficient '],
    righthind_data[righthind_data['Genotype'] == 'T230M'][' Ataxia Coefficient ']
)

print("Right Hind ANOVA p-value:", righthind_anova_result.pvalue)

# %% Plotting for Ataxia Coeff.

fig, ax = plt.subplots(1, 4)
plt.style.use('fivethirtyeight')

# For digigait LF

sns.barplot(data=resultantDF[resultantDF[' Limb ']==' Left Fore '], x='Genotype', y=' Ataxia Coefficient ', ax = ax[0], errwidth=2, capsize=0.4, errorbar = ('se'))
sns.stripplot(data=resultantDF[resultantDF[' Limb ']==' Left Fore '], x='Genotype', y=' Ataxia Coefficient ', dodge=False, ax=ax[0], edgecolor='black', size=2, linewidth=0.5, palette = sns.color_palette())
ax[0].tick_params(axis='x', rotation=45)
ax[0].set_title('Left Fore', fontsize=15, fontweight='bold', fontname='Montserrat')
ax[0].set_xlabel(''  , fontsize = 15, fontname='Montserrat')
ax[0].set_ylabel('Ataxia Coefficient', fontsize = 15, fontname='Montserrat')

# For Digigait LH

sns.barplot(data=resultantDF[resultantDF[' Limb ']==' Left Hind '], x='Genotype', y=' Ataxia Coefficient ', ax = ax[1], errwidth=2, capsize=0.4, errorbar = ('se'))
sns.stripplot(data=resultantDF[resultantDF[' Limb ']==' Left Hind '], x='Genotype', y=' Ataxia Coefficient ', dodge=False, ax=ax[1], edgecolor='black', size=2, linewidth=0.5, palette = sns.color_palette())
ax[1].tick_params(axis='x', rotation=45)
ax[1].set_title('Left Hind', fontsize=15, fontweight='bold', fontname='Montserrat')
ax[1].set_xlabel('', fontsize = 15, fontname='Montserrat')
ax[1].set_ylabel('', fontsize = 15, fontname='Montserrat')


# For Digigait RF

sns.barplot(data=resultantDF[resultantDF[' Limb ']==' Right Fore '], x='Genotype', y=' Ataxia Coefficient ', ax = ax[2], errwidth=2, capsize=0.4, errorbar = ('se'))
sns.stripplot(data=resultantDF[resultantDF[' Limb ']==' Right Fore '], x='Genotype', y=' Ataxia Coefficient ', dodge=False, ax=ax[2], edgecolor='black', size=2, linewidth=0.5, palette = sns.color_palette())
ax[2].tick_params(axis='x', rotation=45)
ax[2].set_title('Right Fore', fontsize=15, fontweight='bold', fontname='Montserrat')
ax[2].set_xlabel('', fontsize = 15, fontname='Montserrat')
ax[2].set_ylabel('', fontsize = 15, fontname='Montserrat')

# For Digigait LH

sns.barplot(data=resultantDF[resultantDF[' Limb ']==' Right Hind '], x='Genotype', y=' Ataxia Coefficient ', ax = ax[3], errwidth=2, capsize=0.4, errorbar = ('se'))
sns.stripplot(data=resultantDF[resultantDF[' Limb ']==' Right Hind '], x='Genotype', y=' Ataxia Coefficient ', dodge=False, ax=ax[3], edgecolor='black', size=2, linewidth=0.5, palette = sns.color_palette())
ax[3].tick_params(axis='x', rotation=45)
ax[3].set_title('Right Hind', fontsize=15, fontweight='bold', fontname='Montserrat')
ax[3].set_xlabel('', fontsize = 15, fontname='Montserrat')
ax[3].set_ylabel('', fontsize = 15, fontname='Montserrat')


plt.tight_layout()
plt.show()

# %% Plotting Paw Angle

fig, ax = plt.subplots(1, 4)
plt.style.use('fivethirtyeight')

# For digigait LF

sns.barplot(data=resultantDF[resultantDF[' Limb ']==' Left Fore '], x='Genotype', y=' PawAngle ', ax = ax[0], errwidth=2, capsize=0.4, errorbar = ('se'))
sns.stripplot(data=resultantDF[resultantDF[' Limb ']==' Left Fore '], x='Genotype', y=' PawAngle ', dodge=False, ax=ax[0], edgecolor='black', size=2, linewidth=0.5, palette = sns.color_palette())
ax[0].tick_params(axis='x', rotation=45)
ax[0].set_title('Left Fore', fontsize=15, fontweight='bold', fontname='Montserrat')
ax[0].set_xlabel(''  , fontsize = 15, fontname='Montserrat')
ax[0].set_ylabel('PawAngle', fontsize = 15, fontname='Montserrat')

# For Digigait LH

sns.barplot(data=resultantDF[resultantDF[' Limb ']==' Left Hind '], x='Genotype', y=' PawAngle ', ax = ax[1], errwidth=2, capsize=0.4, errorbar = ('se'))
sns.stripplot(data=resultantDF[resultantDF[' Limb ']==' Left Hind '], x='Genotype', y=' PawAngle ', dodge=False, ax=ax[1], edgecolor='black', size=2, linewidth=0.5, palette = sns.color_palette())
ax[1].tick_params(axis='x', rotation=45)
ax[1].set_title('Left Hind', fontsize=15, fontweight='bold', fontname='Montserrat')
ax[1].set_xlabel('', fontsize = 15, fontname='Montserrat')
ax[1].set_ylabel('', fontsize = 15, fontname='Montserrat')


# For Digigait RF

sns.barplot(data=resultantDF[resultantDF[' Limb ']==' Right Fore '], x='Genotype', y=' PawAngle ', ax = ax[2], errwidth=2, capsize=0.4, errorbar = ('se'))
sns.stripplot(data=resultantDF[resultantDF[' Limb ']==' Right Fore '], x='Genotype', y=' PawAngle ', dodge=False, ax=ax[2], edgecolor='black', size=2, linewidth=0.5, palette = sns.color_palette())
ax[2].tick_params(axis='x', rotation=45)
ax[2].set_title('Right Fore', fontsize=15, fontweight='bold', fontname='Montserrat')
ax[2].set_xlabel('', fontsize = 15, fontname='Montserrat')
ax[2].set_ylabel('', fontsize = 15, fontname='Montserrat')

# For Digigait LH

sns.barplot(data=resultantDF[resultantDF[' Limb ']==' Right Hind '], x='Genotype', y=' PawAngle ', ax = ax[3], errwidth=2, capsize=0.4, errorbar = ('se'))
sns.stripplot(data=resultantDF[resultantDF[' Limb ']==' Right Hind '], x='Genotype', y=' PawAngle ', dodge=False, ax=ax[3], edgecolor='black', size=2, linewidth=0.5, palette = sns.color_palette())
ax[3].tick_params(axis='x', rotation=45)
ax[3].set_title('Right Hind', fontsize=15, fontweight='bold', fontname='Montserrat')
ax[3].set_xlabel('', fontsize = 15, fontname='Montserrat')
ax[3].set_ylabel('', fontsize = 15, fontname='Montserrat')


plt.tight_layout()
plt.show()
