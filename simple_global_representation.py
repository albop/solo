
def simple_global_representation(self, substitute_auxiliary=False, keep_auxiliary=False, allow_future_shocks=True, solve_systems=False):

    resp = {}
    eq_g = self['equations_groups']
    v_g = self['variables_groups']
    if 'expectation' in eq_g:
        resp['f_eqs'] = [ eq.gap for eq in  eq_g['arbitrage'] + eq_g['expectation']] # TODO: complementarity conditions
        resp['controls'] = v_g['controls'] + v_g['expectations']
    else:
        resp['f_eqs'] = [ eq.gap for eq in  eq_g['arbitrage']] # TODO: complementarity conditions
        resp['controls'] = list( v_g['controls'] )

    resp['g_eqs'] = [eq.rhs for eq in  eq_g['transition'] ]

    if 'auxiliary' in eq_g:
        if not substitute_auxiliary:
            if not keep_auxiliary:
                resp['f_eqs'] += [eq.gap for eq in eq_g['auxiliary']]
                resp['controls'] += v_g['auxiliary']
        else:
            sdict = {}
            from misc import timeshift
            auxies = list( eq_g['auxiliary'] )
            if 'auxiliary_2' in eq_g:
                auxies += list( eq_g['auxiliary_2'] )
            for eq in  auxies:
                sdict[eq.lhs] = eq.rhs
                sdict[eq.lhs(1)] = timeshift( eq.rhs, 1)
                sdict[eq.lhs(-1)] = timeshift( eq.rhs, -1)
            from triangular_solver import solve_triangular_system
            sdict = solve_triangular_system(sdict)
            resp['a_eqs'] = [sdict[v] for v in v_g['auxiliary']]
            resp['auxiliaries'] = [v for v in v_g['auxiliary']]
            resp['f_eqs'] = [eq.subs(sdict) for eq in resp['f_eqs']]
            resp['g_eqs'] = [eq.subs(sdict) for eq in resp['g_eqs']]
    elif 'auxiliary_2' in eq_g:
        sdict = {}
        from dolo.misc.misc import timeshift
        auxies = eq_g['auxiliary_2']
        for eq in  auxies:
            sdict[eq.lhs] = eq.rhs
            sdict[eq.lhs(1)] = timeshift( eq.rhs, 1)
            sdict[eq.lhs(-1)] = timeshift( eq.rhs, -1)
        from dolo.misc.calculus import simple_triangular_solve
        sdict = simple_triangular_solve(sdict)
        resp['f_eqs'] = [eq.subs(sdict) for eq in resp['f_eqs']]
        resp['g_eqs'] = [eq.subs(sdict) for eq in resp['g_eqs']]


    if not allow_future_shocks:
        # future shocks are replaced by 0
        zero_shocks = {s(1):0 for s in self.shocks}
        resp['f_eqs'] = [ eq.subs(zero_shocks) for eq in resp['f_eqs'] ]

    if solve_systems:
        from triangular_solver import solve_triangular_system
        system = {s: resp['g_eqs'][i] for i,s in enumerate(v_g['states'])}
        new_geqs = solve_triangular_system(system)
        resp['g_eqs'] = [new_geqs[s] for s in v_g['states']]

    resp['states'] = v_g['states']
    resp['shocks'] = self.shocks #['shocks_ordering'] # TODO: bad
    resp['parameters'] = self.parameters #['parameters_ordering']
    return resp