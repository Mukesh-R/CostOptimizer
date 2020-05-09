import os
import json

class CostOptimizer:
    '''
    Cost optimizer class which reads the configurations of regions devices & costs
    and calculates the optimized resource allocation.

    Methods:
    --------------------------------
    read_config()
        reads the configuration files
    get_machines()
        returns the machines associated with regions
    get_machine_order()
        return the order of machines to be allocated
    remove_highcost_machines()
        removes the machines which charges high fare
    optimize()
        returns the optimized output for all regions
    '''

    __config_path = ''
    __capacities = None
    __region_costs = None
    __region_machines = {}
    __machine_order = []

    def __new__(cls, *args, **kwargs):
        '''
        Restricts the creation of instance if the config file(s) are not available
        '''
        config_path = '../config'
        if 'config_path' in kwargs.keys():
            config_path = kwargs['config_path']
            kwargs['config_path'] = config_path
        if (not os.path.exists(os.path.join(os.path.abspath(config_path), 'capacities.json'))) \
            or (not os.path.exists(os.path.join(os.path.abspath(config_path), 'region_cost.json'))):
            print('Path/file(s) does not exist!')
            raise FileNotFoundError
        return super(CostOptimizer, cls).__new__(cls)

    def __init__(self, config_path='../config'):
        '''
        Initializes class with the required values

        Parameters
        --------------------------------
        config_path: <str>
            path to config directory
        '''
        super().__init__()
        self.__config_path = config_path
        self.read_configs()
        self.__region_machines = self.get_machines()
        self.__machine_order = self.get_machine_order()
        self.remove_highcost_machines()

    def read_configs(self):
        '''
        Reads the config file
        '''
        try:
            with open(os.path.join(os.path.abspath(self.__config_path), 'capacities.json'), 'r') as capacities_file:
                self.__capacities = json.load(capacities_file)
            with open(os.path.join(os.path.abspath(self.__config_path), 'region_cost.json'), 'r') as cost_file:
                self.__region_costs = json.load(cost_file)
        except Exception as e:
            raise e

    def get_machines(self):
        '''
        Returns the machines associated with region

        Return
        --------------------------------
        machines: <dict>
        '''
        return {region: list(machines.keys()) for region, machines in self.__region_costs.items()}

    def get_machine_order(self):
        '''
        Returns the machine order

        Return
        --------------------------------
        machine_order: <dict>
        '''
        return sorted(list(self.__capacities.keys()), key = lambda x: self.__capacities[x], reverse = True)

    def remove_highcost_machines(self):
        '''
        Removes the machines that cost more from regions
        '''
        for region in self.__region_machines.keys():
            prev_cost = -1
            multiplier = 1
            for machine in self.__machine_order[::-1]:
                if machine in self.__region_machines[region]:
                    if prev_cost == -1:
                        prev_cost = self.__region_costs[region][machine]
                    elif ((prev_cost * multiplier * 2) >= self.__region_costs[region][machine]):
                        prev_cost = self.__region_costs[region][machine]
                        multiplier = 1
                    else:
                        self.__region_machines[region].remove(machine)
                        multiplier += 1
                else:
                    multiplier += 1

    def optimize(self, capacity, hours):
        '''
        Optimizes the resources with the given capacity and hours

        Parameters
        --------------------------------
        capacity: <int>
        hours: <int>

        Return
        --------------------------------
        optimized_output: <dict>
        '''
        if (capacity % 10 != 0):
            print('Capacity can only be multiples of 10!')
            return
        result = []
        for region in self.__region_machines.keys():
            region_optimized_data = {
                'region': region,
                'total_cost': 0,
                'machines': []
            }
            reg_capacity = capacity
            for machine in self.__machine_order:
                if machine in self.__region_machines[region]:
                    count = reg_capacity // self.__capacities[machine]
                    if count == 0:
                        continue
                    reg_capacity = reg_capacity % self.__capacities[machine]
                    region_optimized_data['machines'].append((machine, count))
                    region_optimized_data['total_cost'] += (count * self.__region_costs[region][machine])
                if reg_capacity == 0:
                    break
            
            region_optimized_data['total_cost'] = '$' + str(region_optimized_data['total_cost'] * hours)
            result.append(region_optimized_data)
        return {'Output': result}
