
frames = ['1型CMOS', '23.5mm×15.7mm(APS-Cサイズ) 正方画素CMOS', '1/2.3型CMOS(裏面照射型)', '1型CMOS(裏面照射型)', '1/2.33型CMOS(裏面照射型)', '1/2.3型MOS', '23.5mm×15.6mm(APS-Cサイズ) X-Trans CMOS III', '1型MOS', '1/2.3型CCD', '1/3.1型CMOS', '23.7mm×15.7mm(APS-Cサイズ)CMOS', '22.3mm×14.9mm(APS-Cサイズ)CMOS', '1/1.7型CMOS(裏面照射型)', '35.9mm×24.0mm(フルサイズ) Exmor CMOSセンサー', '1/2.3型CMOSx2', '4/3型(フォーサーズ)MOS', '36mm×24mm(フルサイズ) CMOS', '1.5型CMOS', '1/10型CMOS', '23.6mm×15.6mm(APS-Cサイズ) X-Trans CMOS II', '1/2.33型CMOS', '35.8mm×23.9mm(フルサイズ) Exmor CMOSセンサー', '1/2.3型CMOS', 'CCD', '23.5mm×15.7mm(APS-Cサイズ)CMOS', 'CMOS', '1/5型CMOS', '1/2.33型CCD', 'CMOSx2', 'APS-C型CMOS', 'APS-C22.3mm×14.9mmCMOS', 'フルサイズ35.6mm×23.8mmCMOS', 'フルサイズ36mm×24mmCMOS', 'フォーサーズ4/3型LiveMOS', 'APS-C23.5mm×15.6mmCMOS4', 'APS-C23.5mm×15.6mmCMOS', 'フルサイズ35.9mm×24mmCMOS', 'フルサイズ35.8mm×23.9mmCMOS', 'APS-C23.5mm×15.7mmCMOS', 'APS-C23.6mm×15.6mmCMOSIII', 'APS-C23.5mm×15.6mmCMOSIII', 'フルサイズ35.9mm×24.0mmCMOS', 'フルサイズ35.9mm×23.9mmCMOS', '13.2mm×8.8mmCMOS', 'APS-C23.6mm×15.6mmCMOS', 'APS-C23.6mm×15.6mmCMOSII', '中判サイズFUJIFILM G Format43.8mm×32.9mmベイヤーCMOS', 'APS-H26.7mm×17.9mmCMOS', 'APS-C23.4mm×15.5mmCMOS', '中判サイズ32.9mm×43.8mmCMOS', 'APS-C23.6mm×15.7mmCMOS', 'APS-C22.4mm×15mmCMOS', 'フルサイズ36mm×23.9mmCMOS', '中判サイズ43.8mm×32.8mmCMOS', 'APS-C22.5mm×15.0mmCMOS', '中判サイズ53.4mm×40mmCMOS', 'APS-C23.7mm×15.7mmCMOS', '中判サイズ48mm×36mmCCD', '23.5mm×15.7mmCMOS X3']

dict = {'中判サイズ': [], 'フルサイズ': [], 'APS-C': [], '4/3型': [], '1型': [], '1/2.3型': [], '1/3.1型': [], '1/1.7型': [], '1.5型': [], '1/10型': [], '1/5型': [], 'CMOSx2': []}

print(len(frames))

for frame in frames:
  for key, val in dict.items():
    appended = False
    if key in frame:
      val.append(frame)
      appended = True
      break
  if appended is False:
    print('dictに入らなかった')
    print(frame)

length = 0

for key, val in dict.items():
  print(key)
  print(val)
  length += len(val)
  print("-------------------")

print(length)

print(dict)
