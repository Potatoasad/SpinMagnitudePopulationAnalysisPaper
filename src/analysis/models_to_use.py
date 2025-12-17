from gravpop import *

class TruncatedGaussian2DMixtureZeroAndFloatingIndependent(AnalyticPopulationModel, SpinPopulationModel):
    def __init__(self, a, b, var_names=['chi_1', 'chi_2'], hyper_var_names=['sigma_chi_at_0','mu_chi_1', 'sigma_chi_1', 'mu_chi_2', 'sigma_chi_2', 'rho_chi' 'eta_spin']):
        self.var_names = var_names
        self.hyper_var_names = hyper_var_names
        self.a = a; self.b=b;
        kwargs = {'a' : a, 'b' : b}
        comp1_var_names = [var_names[0]]
        comp2_var_names = [var_names[1]]

        comp1_hyper_var_names = ['mu_zero_spin_1d_fixed', self.hyper_var_names[0], 'mu_zero_spin_1d_fixed', self.hyper_var_names[0], 'rho_zero_fixed']
        comp2_hyper_var_names = self.hyper_var_names[1:6]
        self.mixture_hyper_var_name = self.hyper_var_names[-1]

        self.models = [TruncatedGaussian2DAnalytic(var_names=self.var_names, hyper_var_names=comp1_hyper_var_names, a=a, b=b),
                       TruncatedGaussian2DAnalytic(var_names=self.var_names, hyper_var_names=comp2_hyper_var_names, a=a, b=b)]

    @property
    def limits(self):
        return {var : [self.a[i], self.b[i]] for i,var in enumerate(self.var_names)}

    def __call__(self, data, params):
        params['mu_zero_spin_1d_fixed'] = 0.0
        params['rho_zero_fixed'] = 1e-6
        result  =      params[self.mixture_hyper_var_name]  * self.models[0](data, params)
        result += (1 - params[self.mixture_hyper_var_name]) * self.models[1](data, params)
        return result

    def evaluate(self, data, params):
        params['mu_zero_spin_1d_fixed'] = 0.0
        params['rho_zero_fixed'] = 1e-6
        result  =      params[self.mixture_hyper_var_name]  * self.models[0].evaluate(data, params)
        result += (1 - params[self.mixture_hyper_var_name]) * self.models[1].evaluate(data, params)
        return result


class TruncatedGaussian1DMixtureZeroAndFloatingIndependent(AnalyticPopulationModel, SpinPopulationModel):
    def __init__(self, a, b, var_names=['chi_1', 'chi_2'], hyper_var_names=['sigma_chi_at_0','mu_chi_1', 'sigma_chi_1', 'mu_chi_2', 'sigma_chi_2', 'eta_spin']):
        self.var_names = var_names
        self.hyper_var_names = hyper_var_names
        self.a = a; self.b=b;
        kwargs = {'a' : a, 'b' : b}
        comp1_var_names = [var_names[0]]
        comp2_var_names = [var_names[1]]

        comp1_hyper_var_names = ['mu_zero_spin_1d_fixed', self.hyper_var_names[0], 'mu_zero_spin_1d_fixed', self.hyper_var_names[0]]
        comp2_hyper_var_names = self.hyper_var_names[1:5]
        self.mixture_hyper_var_name = self.hyper_var_names[-1]

        self.models = [TruncatedGaussian1DIndependentAnalytic(var_names=self.var_names, hyper_var_names=comp1_hyper_var_names, a=a, b=b),
                       TruncatedGaussian1DIndependentAnalytic(var_names=self.var_names, hyper_var_names=comp2_hyper_var_names, a=a, b=b)]

    @property
    def limits(self):
        return {var : [self.a, self.b] for i,var in enumerate(self.var_names)}

    def __call__(self, data, params):
        params['mu_zero_spin_1d_fixed'] = 0.0
        result  =      params[self.mixture_hyper_var_name]  * self.models[0](data, params)
        result += (1 - params[self.mixture_hyper_var_name]) * self.models[1](data, params)
        return result

    def evaluate(self, data, params):
        params['mu_zero_spin_1d_fixed'] = 0.0
        result  =      params[self.mixture_hyper_var_name]  * self.models[0].evaluate(data, params)
        result += (1 - params[self.mixture_hyper_var_name]) * self.models[1].evaluate(data, params)
        return result
    
    
class TruncatedGaussian1DIndependentAnalyticVariedLimits(AnalyticPopulationModel, SpinPopulationModel):
    def __init__(self, a, b, var_names=['chi_1', 'chi_2'], hyper_var_names=['mu_chi_1', 'sigma_chi_1', 'chi_1_min', 'chi_1_max',
                                                                            'mu_chi_2', 'sigma_chi_2', 'chi_2_min', 'chi_2_max']):
        self.a, self.b = a,b
        self.var_names = var_names
        self.hyper_var_names = hyper_var_names
        kwargs = {'a' : a, 'b' : b}
        self.models = [TruncatedGaussian1DAnalyticVariedLimits(var_names=[var_names[i]],
                                                   hyper_var_names=[hyper_var_names[2*i], hyper_var_names[2*i + 1], hyper_var_names[2*i + 2], hyper_var_names[2*i + 3]],
                                                   **kwargs) for i in range(len(self.var_names))]
    @property
    def limits(self):
        return {var : [self.a, self.b] for i,var in enumerate(self.var_names)}

    def __call__(self, data, params):
        result = self.models[0](data, params)
        for i in range(1,len(self.models)):
            result *= self.models[i](data, params)
        return result

    def evaluate(self, data, params):
        result = self.models[0].evaluate(data, params)
        for i in range(1,len(self.models)):
            result *= self.models[i].evaluate(data, params)
        return result

    def sample(self, df_hyper_samples, oversample=1):
        return ppd_truncUncorrelatedanalytic(self, df_hyper_samples, oversample=oversample)