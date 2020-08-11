#ifndef _PATCH_ENERGY_POLYDISPERSE_12_H_
#define _PATCH_ENERGY_POLYDISPERSE_12_H_

#include "hoomd/HOOMDMath.h"
#include "hoomd/VectorMath.h"
#include "IntegratorHPMCSwap.h"

// A Place Holder which adds more functions to the PatchEnergyJIT
class PatchEnergyPolydisperse12 : public hpmc::PatchEnergy
{
    public:
        //! Constructor
        PatchEnergyPolydisperse12(Scalar _v0, Scalar _eps, Scalar _scaledrcut, Scalar kT)
            : v0(_v0/kT), eps(_eps), scaledr_cut(_scaledrcut), c0(Scalar(-1.92415)), c1(Scalar(2.11106)), c2(Scalar(-0.591097))
        {
                c0 =  Scalar(-28.0)*v0/(kT*pow(scaledr_cut,12));
                c1 =  Scalar(48.0)*v0/(kT*pow(scaledr_cut,14));
                c2 =  Scalar(-21.0)*v0/(kT*pow(scaledr_cut,16));
        }
        ~PatchEnergyPolydisperse12(){};
        //! Get the maximum r_ij radius beyond which energies are always 0
        virtual Scalar getScaledRCut()
        {
            return scaledr_cut;
        }

        //! Get the maximum r_ij radius beyond which energies are always 0
        virtual inline Scalar getAdditiveCutoff(unsigned int type)
        {
            // this potential corresponds to a point particle
            return 0.0;
        }

        //! evaluate the energy of the patch interaction
        /*! \param r_ij Vector pointing from particle i to j
            \param type_i Integer type index of particle i
            \param d_i Diameter of particle i
            \param charge_i Charge of particle i
            \param q_i Orientation quaternion of particle i
            \param type_j Integer type index of particle j
            \param q_j Orientation quaternion of particle j
            \param d_j Diameter of particle j
            \param charge_j Charge of particle j
            \returns Energy of the patch interaction.
        */
        virtual float energy(const vec3<float>& r_ij,
            unsigned int type_i,
            const quat<float>& q_i,
            float d_i,
            float charge_i,
            unsigned int type_j,
            const quat<float>& q_j,
            float d_j,
            float charge_j)
            {
                Scalar rsq = dot(r_ij, r_ij);
                Scalar sigma  = 0.5*( d_i+d_j)*(1-eps*fabs(d_i-d_j));
                Scalar rcut  = scaledr_cut*(sigma);
                if (rsq <= rcut*rcut)
                {
                    Scalar sigmasq = sigma*sigma;
                    Scalar rsqinv = sigmasq / rsq;
                    Scalar _rsq = rsq / sigmasq;
                    Scalar r6inv = rsqinv*rsqinv*rsqinv;
                    return v0*r6inv*r6inv+c0+c1*_rsq+c2*_rsq*_rsq;
                }
                else
                {
                    return 0.0;
                }
            }

    protected:
        // A Bunch of parameters
        Scalar v0;
        Scalar eps;
        Scalar scaledr_cut;                             //!< Cutoff radius scaled with respect to sigma_{ij}
        Scalar c0;
        Scalar c1;
        Scalar c2;
};

//! Exports the PatchEnergyPolydisperse12 class to python
void export_PatchEnergyPolydisperse12(pybind11::module &m)
{
    pybind11::class_<PatchEnergyPolydisperse12, std::shared_ptr<PatchEnergyPolydisperse12> >(m, "PatchEnergyPolydisperse12", pybind11::base< hpmc::PatchEnergy >())
        .def(pybind11::init< Scalar, Scalar, Scalar, Scalar >())
        .def("getScaledRCut", &PatchEnergyPolydisperse12::getScaledRCut)
        .def("energy", &PatchEnergyPolydisperse12::energy);
}
#endif // _PATCH_ENERGY_POLYDISPERSE_12_H_
