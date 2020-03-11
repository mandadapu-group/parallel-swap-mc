// Copyright (c) 2009-2019 The Regents of the University of Michigan
// This file is part of the HOOMD-blue project, released under the BSD 3-Clause License.

#ifndef _HPMC_COUNTERS_SWAP_H_
#define _HPMC_COUNTERS_SWAP_H_

#include <hoomd/hpmc/HPMCCounters.h>
//#include "hoomd/HOOMDMath.h"

namespace hpmc
{

/*! \file HPMCCountersSwap.h
    \brief Declaration of counters whatnot
    In the next implementation, I will need to get counters to do count swap moves but for now, it'll just inherit everything that hpmc_counters_t has
*/

// need to declare these class methods with __device__ qualifiers when building in nvcc
// DEVICE is __host__ __device__ when included in nvcc and blank when included into the host compiler
#ifdef NVCC
#define DEVICE __device__
#else
#define DEVICE
#endif

//! Storage for acceptance counters
/*! \ingroup hpmc_data_structs */
struct hpmc_counters_swap_t : hpmc_counters_t
    {
    unsigned long long int swap_accept_count;      //!< Count of accepted translation moves
    unsigned long long int swap_reject_count;      //!< Count of rejected translation moves

    //! Construct a zero set of counters
    hpmc_counters_swap_t()
        {
        swap_accept_count = 0;
        swap_reject_count = 0;
        }

    //! Get the translate acceptance
    /*! \returns The ratio of translation moves that are accepted, or 0 if there are no translation moves
    */
    DEVICE double getSwapAcceptance()
        {
        if (swap_reject_count + swap_accept_count == 0)
            return 0.0;
        else
            return double(swap_accept_count) / double(swap_reject_count + swap_accept_count);
        }

    //! Get the number of moves
    /*! \return The total number of moves
    */
    DEVICE unsigned long long int getNMoves()
        {
        return translate_accept_count + translate_reject_count;//# + swap_accept_count + swap_reject_count;
        }
    };

//! Take the difference of two sets of counters
DEVICE inline hpmc_counters_swap_t operator-(const hpmc_counters_swap_t& a, const hpmc_counters_swap_t& b)
    {
    hpmc_counters_swap_t result;
    result.translate_accept_count = a.translate_accept_count - b.translate_accept_count;
    result.rotate_accept_count = a.rotate_accept_count - b.rotate_accept_count;
    result.swap_accept_count = a.swap_accept_count - b.swap_accept_count;
    result.translate_reject_count = a.translate_reject_count - b.translate_reject_count;
    result.rotate_reject_count = a.rotate_reject_count - b.rotate_reject_count;
    result.swap_reject_count = a.swap_reject_count - b.swap_reject_count;
    result.overlap_checks = a.overlap_checks - b.overlap_checks;
    result.overlap_err_count = a.overlap_err_count - b.overlap_err_count;
    return result;
    }

//! Storage for NPT acceptance counters
/*! \ingroup hpmc_data_structs */
struct hpmc_boxmc_counters_swap_t : hpmc_boxmc_counters_t
    {
    };

//! Take the difference of two sets of counters
DEVICE inline hpmc_boxmc_counters_swap_t operator-(const hpmc_boxmc_counters_swap_t& a, const hpmc_boxmc_counters_swap_t& b)
    {
    hpmc_boxmc_counters_swap_t result;
    result.volume_accept_count = a.volume_accept_count - b.volume_accept_count;
    result.ln_volume_accept_count = a.ln_volume_accept_count - b.ln_volume_accept_count;
    result.shear_accept_count = a.shear_accept_count - b.shear_accept_count;
    result.aspect_accept_count = a.aspect_accept_count - b.aspect_accept_count;
    result.volume_reject_count = a.volume_reject_count - b.volume_reject_count;
    result.ln_volume_reject_count = a.ln_volume_reject_count - b.ln_volume_reject_count;
    result.shear_reject_count = a.shear_reject_count - b.shear_reject_count;
    result.aspect_reject_count = a.aspect_reject_count - b.aspect_reject_count;
    return result;
    }
} // end namespace hpmc

#endif // _HPMC_COUNTERS_SWAP_H_
