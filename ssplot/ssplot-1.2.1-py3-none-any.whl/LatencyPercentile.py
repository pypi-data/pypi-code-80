"""
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * - Redistributions of source code must retain the above copyright notice, this
 * list of conditions and the following disclaimer.
 *
 * - Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * - Neither the name of prim nor the names of its contributors may be used to
 * endorse or promote products derived from this software without specific prior
 * written permission.
 *
 * See the NOTICE file distributed with this work for additional information
 * regarding copyright ownership.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
"""

import ssplot

class LatencyPercentile(ssplot.CommandLine):
  """
  This class is a command line interface to generate a latency percentile
  distribution plot.
  """

  NAME = 'latency-percentile'
  ALIASES = ['latperc', 'lpc']

  @staticmethod
  def create_parser(subparser):
    sp = subparser.add_parser(LatencyPercentile.NAME,
                              aliases=LatencyPercentile.ALIASES,
                              help=('Generate a latency percentile '
                                    'distribution plot'))
    sp.set_defaults(func=LatencyPercentile.run_command)

    sp.add_argument('ifile',
                    help='input latency file')
    sp.add_argument('plotfile',
                    help='output plot file')

    ssplot.LatencyPlot.add_args(LatencyPercentile.NAME, sp)

  @staticmethod
  def run_command(args, plt):
    # create a sample stats object of latencies
    lstats = ssplot.SampleStats(args.ifile)

    # plot
    lp = ssplot.LatencyPlot(plt, LatencyPercentile.NAME, lstats)
    lp.plot(args.plotfile, args)

    return 0


ssplot.CommandLine.register(LatencyPercentile)
