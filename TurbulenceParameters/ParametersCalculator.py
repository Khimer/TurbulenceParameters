import numpy as np


class ParametersCalculator():
    def __init__(self):
        self.constants = [0.0125, 331, 1.225, 1]

    def calculate(self, data):
        dt = self.constants[0]
        # Загрузка данных с сервера
        c = self.constants[1]  # с - скоррость звука (должно быть среднее)
        p = self.constants[2]  # р - плотность воздуха
        cp = self.constants[3]  # Ср - удельная теплоемкость воздуха при постоянном давлении
        # Полная энергия турбулентных движений
        total_energy_of_turbulent_movements = \
            (np.sum(((data[1] - np.mean(data[1])) ** 2)) / (len(data[1]) - 1) +
             np.sum(((data[2] - np.mean(data[2])) ** 2)) / (len(data[2]) - 1) +
             np.sum(((data[3] - np.mean(data[3])) ** 2)) / (len(data[3]) - 1)) / 2
        # Модуль среднего вектора скорости ветра
        module_of_the_average_wind_speed_vector = (np.mean(data[1]) ** 2 + np.mean(data[2]) ** 2 + np.mean(
            data[3]) ** 2) ** 0.5
        # Относительная интенсивность флуктуаций скорости ветра
        relative_intensity_of_fluctuations_in_wind_speed = total_energy_of_turbulent_movements / \
                                                           module_of_the_average_wind_speed_vector ** 2
        # Энергия температурных флуктуаций
        energy_of_temperature_fluctuations = (np.sum((data[0] - np.mean(data[0])) ** 2) / (len(data[0]) - 1)) / 2
        # Пульсация южного компонента ветра
        ripple_of_the_southern_component = (data[1] - np.mean(data[1]))
        # Момент потока импульса
        pulse_flow_moment = np.mean(ripple_of_the_southern_component * (data[3] - np.mean(data[3])))
        # Средняя температура
        average_air_temperature = np.mean(data[0])
        # Пульсация температуры
        temperature_ripple = (data[0] - average_air_temperature)
        # Момент потока тепла
        heat_flow_moment = np.mean(temperature_ripple * (data[3] - np.mean(data[3])))
        # Вертикальный поток импульса
        vertical_impulse_flow = -p * pulse_flow_moment
        # Вертикальный поток тепла
        vertical_heat_flow = cp * p * heat_flow_moment
        # Скорость трения (масштаб ветра)
        friction_speed = (-(pulse_flow_moment)) ** 0.5
        # Масштаб температуры
        temperature_scale = -heat_flow_moment / friction_speed
        # Масштаб Монина-Обухова
        monin_obukhov_scale = average_air_temperature * friction_speed ** 2 / (0.4 * 9.81 * temperature_scale)
        # Коэффициент сопротивления потоку
        flow_resistance_coefficient = (
                                              friction_speed / module_of_the_average_wind_speed_vector) ** 2
        # Структурная постоянная температурных флуктуаций
        # structural_constant_of_temperature_fluctuations = np.mean((temperature_ripple[dt::dt] -
        #     temperature_ripple[0:len(temperature_ripple)-dt:dt])**2)/(module_of_the_average_wind_speed_vector*dt)**(-2/3)
        # # Структурная постоянная ветровых флуктуаций
        # structural_constant_of_wind_fluctuations = np.mean((ripple_of_the_southern_component[dt::dt] -
        #     ripple_of_the_southern_component[0:len(ripple_of_the_southern_component)-dt:dt])**2)/\
        #     (module_of_the_average_wind_speed_vector*dt)**(-2/3)
        # Структурная постоянная температурных флуктуаций
        structural_constant_of_temperature_fluctuations = np.mean((temperature_ripple[1::1] -
                                                                   temperature_ripple[
                                                                   0:len(temperature_ripple) - 1:1]) ** 2) / (
                                                                  module_of_the_average_wind_speed_vector * dt) ** (
                                                                  -2 / 3)
        # Структурная постоянная ветровых флуктуаций
        structural_constant_of_wind_fluctuations = np.mean((ripple_of_the_southern_component[1::1] -
                                                            ripple_of_the_southern_component[
                                                            0:len(ripple_of_the_southern_component) - 1:1]) ** 2) / \
                                                   (module_of_the_average_wind_speed_vector * dt) ** (-2 / 3)
        # Структурная постоянная флуктуаций акустического показателя п реломления
        structural_constant_of_fluctuations_of_the_acoustic_refractive_index = \
            structural_constant_of_temperature_fluctuations / \
            (2 * (average_air_temperature + 273.15)) ** 2 + structural_constant_of_wind_fluctuations / c ** 2
        # Структурная постоянная флуктуаций оптического показателя преломления
        structural_constant_of_fluctuations_of_the_optical_refractive_index = \
            structural_constant_of_temperature_fluctuations * \
            (8 * 10 ** (-5) * np.mean(data[4]) * 1.33322 / (average_air_temperature + 273.15) ** 2) ** 2

        return [total_energy_of_turbulent_movements, relative_intensity_of_fluctuations_in_wind_speed,
                energy_of_temperature_fluctuations, pulse_flow_moment, heat_flow_moment, vertical_impulse_flow,
                vertical_heat_flow, friction_speed, temperature_scale, monin_obukhov_scale, flow_resistance_coefficient,
                structural_constant_of_temperature_fluctuations, structural_constant_of_wind_fluctuations,
                structural_constant_of_fluctuations_of_the_acoustic_refractive_index,
                structural_constant_of_fluctuations_of_the_optical_refractive_index]