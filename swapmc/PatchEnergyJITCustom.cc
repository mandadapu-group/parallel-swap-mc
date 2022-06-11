#include "PatchEnergyJITCustom.h"
#include "hoomd/jit/EvalFactory.h"

#include <sstream>

#define PATCH_ENERGY_LOG_NAME           "patch_energy"
#define PATCH_ENERGY_RCUT               "patch_energy_rcut"

/*! \param exec_conf The execution configuration (used for messages and MPI communication)
    \param llvm_ir Contents of the LLVM IR to load
    \param r_cut Center to center distance beyond which the patch energy is 0

    After construction, the LLVM IR is loaded, compiled, and the energy() method is ready to be called.
*/
PatchEnergyJITCustom::PatchEnergyJITCustom(std::shared_ptr<ExecutionConfiguration> exec_conf, const std::string& llvm_ir, Scalar scaledr_cut) : m_scaledr_cut(scaledr_cut)
    {
    // build the JIT.
    m_factory = std::shared_ptr<EvalFactory>(new EvalFactory(llvm_ir));

    // get the evaluator
    m_eval = m_factory->getEval();

    if (!m_eval)
        {
        exec_conf->msg->error() << m_factory->getError() << std::endl;
        throw std::runtime_error("Error compiling JIT code.");
        }
    }


void export_PatchEnergyJITCustom(pybind11::module &m)
    {
      pybind11::class_<hpmc::PatchEnergy, std::shared_ptr<hpmc::PatchEnergy> >(m, "PatchEnergy")
              .def(pybind11::init< >());
    pybind11::class_<PatchEnergyJITCustom, std::shared_ptr<PatchEnergyJITCustom> >(m, "PatchEnergyJITCustom", pybind11::base< hpmc::PatchEnergy >())
            .def(pybind11::init< std::shared_ptr<ExecutionConfiguration>,
                                 const std::string&,
                                 Scalar >())
            .def("getScaledRCut", &PatchEnergyJITCustom::getScaledRCut)
            .def("energy", &PatchEnergyJITCustom::energy);
    }
