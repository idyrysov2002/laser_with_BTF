
# from mock_devices.oscilloscope.oscilloscope_lib import Oscilloscope
# from devices.oscilloscope.oscilloscope_measure_lib import oscilloscope_measurement
# from scripts.create_date_folder import create_date_folder
# # Настройки
# osciloscope_IP = "10.2.60.150"
# osciloscope_PORT = 4000
# osciloscope_CHANNEL = 4 # Измените на нужный канал
# main_folder = create_date_folder(
#         base_path=r"C:\Users\namys_5zzf7sz\OneDrive\Документы\DATA\data_for_testing", prefix="exp_simulator")
# # Инициализация соединения
# delay=300
# current=400
# voltage=0

# osc = Oscilloscope(ip=osciloscope_IP, port=osciloscope_PORT)
# osc_filename=f'osc_spectrum_delay_{delay}ps_current_{current}mA_voltage_{voltage}V'

yokogawa_folder_name=f'voltage_{voltage}V/yokogawa_measurements/current_{current}mA'
yokogawa_folder_path=create_subfolder(parent_folder_path=main_folder, subfolder_name=yokogawa_folder_name)

# Создаем папки для каждого спана
yokogawa_big_span_folder_path=create_subfolder(parent_folder_path=yokogawa_folder_path, subfolder_name=yokogawa_big_span_name)
yokogawa_small_span_folder_path=create_subfolder(parent_folder_path=yokogawa_folder_path, subfolder_name=yokogawa_small_span_name)

# название файлов
yokogawa_big_span_filename=f'yokogawa_spectrum_delay_{delay}ps_current_{current}mA_voltage_{voltage}V_{yokogawa_big_span_name}'
yokogawa_small_span_filename=f'yokogawa_spectrum_delay_{delay}ps_current_{current}mA_voltage_{voltage}V_{yokogawa_small_span_name}'

# Большой спан
yokogawa_peak_wave_big, yokogawa_peak_ampl_big = osa_measurement(
yokogawa_devices=devices["yokogawa"],
folder_path=yokogawa_big_span_folder_path,
filename=yokogawa_big_span_filename,
res=YOKOGAWA_RES_BIG_SPAN,
wave_start=YOKOGAWA_BIG_SPAN_START,
wave_stop=YOKOGAWA_BIG_SPAN_STOP,
save_png=True,
)

yokogawa_peak_wave_big_data.append(yokogawa_peak_wave_big)
yokogawa_peak_ampl_big_data.append(yokogawa_peak_ampl_big)

YOKOGAWA_SMALL_SPAN_START = yokogawa_peak_wave_big - 2 * linewidth
YOKOGAWA_SMALL_SPAN_STOP = yokogawa_peak_wave_big + 2 * linewidth

# Малый спан
yokogawa_peak_wave_small, yokogawa_peak_ampl_small = osa_measurement(
yokogawa_devices=devices["yokogawa"],
folder_path=yokogawa_small_span_folder_path,
filename=yokogawa_small_span_filename,
res=YOKOGAWA_RES_SMALL_SPAN,
wave_start=YOKOGAWA_SMALL_SPAN_START,
wave_stop=YOKOGAWA_SMALL_SPAN_STOP,
save_png=True,
)
yokogawa_peak_wave_small_data.append(yokogawa_peak_wave_small)
yokogawa_peak_ampl_small_data.append(yokogawa_peak_ampl_small)
