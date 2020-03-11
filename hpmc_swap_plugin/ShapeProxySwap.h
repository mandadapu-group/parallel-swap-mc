// Copyright (c) 2009-2019 The Regents of the University of Michigan
// This file is part of the HOOMD-blue project, released under the BSD 3-Clause License.

#ifndef __SHAPE_PROXY_SWAP_H__
#define __SHAPE_PROXY_SWAP_H__

#include "IntegratorHPMCPolydisperse.h"
#include "ShapePolydisperse.h"
#include <hoomd/extern/pybind/include/pybind11/stl.h>

#ifndef NVCC
#include <hoomd/extern/pybind/include/pybind11/pybind11.h>
#endif

namespace hpmc{

namespace detail{

    #define IGNORE_STATS 0x0001
    template< typename Shape >
    struct get_param_data_type { typedef typename Shape::param_type type; };
    
    template< typename Shape >
    struct access
        {
        template< class ParamType >
        typename get_param_data_type<Shape>::type& operator()(ParamType& param) { return param; }
        template< class ParamType >
        const typename get_param_data_type<Shape>::type& operator()(const ParamType& param) const  { return param; }
        };

    //! Helper function to build sph_params from python
    sph_poly_params make_sph_poly_params(bool ignore_stats, OverlapReal max_radius, OverlapReal min_radius, bool orientable)
        {
        sph_poly_params result;
        result.ignore = ignore_stats;
        result.isOriented = orientable;
        result.max_radius = max_radius;
        result.min_radius = min_radius;
        return result;
        }
    
    template < typename Shape , typename AccessType = access<Shape> >
    class shapeswap_param_proxy // base class to avoid adding the ignore flag logic to every other class and holds the integrator pointer + typeid. But now, it's taking in IntegratorHPMCPolydisperse instead
    {
    protected:
        typedef typename Shape::param_type param_type;
    public:
        shapeswap_param_proxy(std::shared_ptr< IntegratorHPMCPolydisperse<Shape> > mc, unsigned int typendx, const AccessType& acc = AccessType()) : m_mc(mc), m_typeid(typendx), m_access(acc) {}
        //!Ignore flag for acceptance statistics
        bool getIgnoreStatistics() const
            {
            std::vector<param_type, managed_allocator<param_type> > & params = m_mc->getParams();
            return (m_access(params[m_typeid]).ignore & IGNORE_STATS);
            }

        void setIgnoreStatistics(bool stat)
            {
            std::vector<param_type, managed_allocator<param_type> > & params = m_mc->getParams();
            if(stat)    m_access(params[m_typeid]).ignore |= IGNORE_STATS;
            else        m_access(params[m_typeid]).ignore &= ~IGNORE_STATS;
            }

    protected:
        std::shared_ptr< IntegratorHPMCPolydisperse<Shape> > m_mc;
        unsigned int m_typeid;
        AccessType m_access;
    };

    
    template<class Shape, class AccessType = access<Shape> >
    class sph_poly_param_proxy : public shapeswap_param_proxy<Shape, AccessType>
    {
    using shapeswap_param_proxy<Shape, AccessType>::m_mc;
    using shapeswap_param_proxy<Shape, AccessType>::m_typeid;
    using shapeswap_param_proxy<Shape, AccessType>::m_access;
    protected:
        typedef typename Shape::param_type  param_type;
    public:
        typedef sph_poly_params access_type;
        sph_poly_param_proxy(std::shared_ptr< IntegratorHPMCPolydisperse<Shape> > mc, unsigned int typendx, const AccessType& acc = AccessType()) : shapeswap_param_proxy<Shape, AccessType>(mc,typendx,acc){}
        /*
        OverlapReal getDiameter()
            {
            std::vector<param_type, managed_allocator<param_type> > & params = m_mc->getParams();
            return OverlapReal(2.0)*m_access(params[m_typeid]).radius;
            }
        */
        bool getOrientable()
            {
            std::vector<param_type, managed_allocator<param_type> > & params = m_mc->getParams();
            return m_access(params[m_typeid]).isOriented;
            }
    };
} //end of namespace detail

template<class Shape, class AccessType>
void export_shapeswap_param_proxy(pybind11::module& m, const std::string& name)
    {
    // export the base class
    // the detail namespace should be imported from the ShapeProxy.h.
    using detail::shapeswap_param_proxy;
    pybind11::class_<shapeswap_param_proxy<Shape, AccessType>, std::shared_ptr< shapeswap_param_proxy<Shape, AccessType> > >(m, name.c_str())
    .def(pybind11::init<std::shared_ptr< IntegratorHPMCPolydisperse<Shape> >, unsigned int>())
    .def_property("ignore_statistics", &shapeswap_param_proxy<Shape, AccessType>::getIgnoreStatistics, &shapeswap_param_proxy<Shape, AccessType>::setIgnoreStatistics)
    ;
    }


template<class ShapeType, class AccessType>
void export_sph_poly_proxy(pybind11::module& m, const std::string& class_name)
    {
    using detail::shapeswap_param_proxy;
    using detail::sph_poly_param_proxy;
    typedef shapeswap_param_proxy<ShapeType, AccessType>    proxy_base;
    typedef sph_poly_param_proxy<ShapeType, AccessType>   proxy_class;
    std::string base_name=class_name+"_base";

    export_shapeswap_param_proxy<ShapeType, AccessType>(m, base_name);
    pybind11::class_<proxy_class, std::shared_ptr< proxy_class > >(m, class_name.c_str(), pybind11::base< proxy_base >())
    .def(pybind11::init<std::shared_ptr< IntegratorHPMCPolydisperse<ShapeType> >, unsigned int>())
    //.def_property_readonly("diameter", &proxy_class::getDiameter)
    .def_property_readonly("orientable", &proxy_class::getOrientable)
    ;
    }

void export_sph_poly_params(pybind11::module& m)
    {
    export_sph_poly_proxy<ShapePolydisperse, detail::access<ShapePolydisperse> >(m, "sph_poly_param_proxy");
    }

} // end namespace hpmc

#endif // end __SHAPE_PROXY_SWAP_H__
