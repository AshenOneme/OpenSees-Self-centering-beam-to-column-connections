import openseespy.opensees as ops
import openseespy.postprocessing.ops_vis as opsv
import matplotlib.pyplot as plt
import openseespy.postprocessing.Get_Rendering as opsplt
import math

ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 3)  # frame 2D

print("****************************************","Material","****************************************")
IDSteel = 1
Fy_Steel = 400
E0_Steel = 210000
bs_Steel = 0.005
R0 = 12.5
cR1 = 0.925
cR2 = 0.15
ops.uniaxialMaterial('Steel02', IDSteel, Fy_Steel, E0_Steel, bs_Steel, R0, cR1, cR2)

IDCoverC = 2
fpc_cover = -28.32
epsc0_cover = -0.0038
fpcu_cover = -8
epsU_cover = -0.02
ops.uniaxialMaterial('Concrete01', IDCoverC, fpc_cover, epsc0_cover, fpcu_cover, epsU_cover)

IDCoreC = 3
fpc_core = -58
epsc0_core = -0.0044
fpcu_core = -22
epsU_core = -0.04
ops.uniaxialMaterial('Concrete01', IDCoreC, fpc_core, epsc0_core, fpcu_core, epsU_core)

# GAP
IDGap = 4
ops.uniaxialMaterial('ElasticPPGap',IDGap,210000,-400,0,1/1000,"noDamage")

IDPT = 5
Fy_PT = 1720
E0_PT = 210000
bs_PT = 0.001
R0 = 12.5
cR1 = 0.925
cR2 = 0.15
a1=0
a2=1
a3=0
a4=1
sigInit=550
ops.uniaxialMaterial('Steel02', IDPT, Fy_PT, E0_PT, bs_PT,R0,cR1,cR2,a1,a2,a3,a4,sigInit)

IDDamper = 6
Fy_Damper = 45160
Fu_Damper=65000
E0_Damper = 70780
bs_Damper = 0.02769
Esh_Damper=1960
eps_sh=0.64
eps_ult=10
R0 = 18
cR1 = 0.925
cR2 = 0.15
ops.uniaxialMaterial('Steel02', IDDamper, Fy_Damper, E0_Damper, bs_Damper,R0, cR1, cR2)

print("****************************************","Section","****************************************")
#Column
Bcol = 400
Hcol = Bcol
#cover
c=25
y1col = Hcol/2.0
z1col = Bcol/2.0
y2col = 0.5*(Hcol-2*c)/3.0
nFibZ=1
nFib=20
nFibCover, nFibCore = 2, 16
As_bar1 = 200.96
As_bar2 = 78.5

fiber_column_section=1
ops.section('Fiber', fiber_column_section)
ops.patch('rect', IDCoreC, nFibCore, nFibZ, c-y1col, c-z1col, y1col-c, z1col-c)
ops.patch('rect', IDCoverC, nFib, nFibZ, -y1col, -z1col, y1col, c-z1col)
ops.patch('rect', IDCoverC, nFib, nFibZ, -y1col, z1col-c, y1col, z1col)
ops.patch('rect', IDCoverC, nFibCover, nFibZ, -y1col, c-z1col, c-y1col, z1col-c)
ops.patch('rect', IDCoverC, nFibCover, nFibZ, y1col-c, c-z1col, y1col, z1col-c)
ops.layer('straight', IDSteel, 4, As_bar1, y1col-c, z1col-c, y1col-c, c-z1col)
ops.layer('straight', IDSteel, 2, As_bar1, y2col, z1col-c, y2col, c-z1col)
ops.layer('straight', IDSteel, 2, As_bar1, -y2col, z1col-c, -y2col, c-z1col)
ops.layer('straight', IDSteel, 4, As_bar1, c-y1col, z1col-c, c-y1col, c-z1col)

#Beam
Bbeam = 250
Hbeam = 400
#cover
c=25
y1beam = Hbeam/2.0
z1beam = Bbeam/2.0
y2beam = 0.5*(Hbeam-2*c)/3.0
z2beam = 0.5*(Bbeam-2*c)/1.0
nFibZ=1
nFib=20
nFibCover, nFibCore = 2, 16
As_bar1 = 200.96
As_bar2 = 78.5

fiber_beam_section=2
ops.section('Fiber', fiber_beam_section)
ops.patch('rect', IDCoreC, nFibCore, nFibZ, c-y1beam, c-z1beam, y1beam-c, z1beam-c)
ops.patch('rect', IDCoverC, nFib, nFibZ, -y1beam, -z1beam, y1beam, c-z1beam)
ops.patch('rect', IDCoverC, nFib, nFibZ, -y1beam, z1beam-c, y1beam, z1beam)
ops.patch('rect', IDCoverC, nFibCover, nFibZ, -y1beam, c-z1beam, c-y1beam, z1beam-c)
ops.patch('rect', IDCoverC, nFibCover, nFibZ, y1beam-c, c-z1beam, y1beam, z1beam-c)
ops.layer('straight',  IDSteel, 4, As_bar1, -y1beam+c, -z2beam, y1beam-c, -z2beam)
ops.layer('straight',  IDSteel, 2, As_bar2, -y1beam+c, 0, y1beam-c, 0)
ops.layer('straight',  IDSteel, 4, As_bar1, -y1beam+c, z2beam, y1beam-c, z2beam)

#Gap
fiber_beam_gap_section=3
ops.section('Fiber', fiber_beam_gap_section)
ops.patch('rect', IDCoreC, nFibCore, nFibZ, c-y1beam, c-z1beam, y1beam-c, z1beam-c)
ops.patch('rect', IDCoverC, nFib, nFibZ, -y1beam, -z1beam, y1beam, c-z1beam)
ops.patch('rect', IDCoverC, nFib, nFibZ, -y1beam, z1beam-c, y1beam, z1beam)
ops.patch('rect', IDCoverC, nFibCover, nFibZ, -y1beam, c-z1beam, c-y1beam, z1beam-c)
ops.patch('rect', IDCoverC, nFibCover, nFibZ, y1beam-c, c-z1beam, y1beam, z1beam-c)
ops.layer('straight', IDGap, 4, As_bar1, -y1beam+c, -z2beam, y1beam-c, -z2beam)
ops.layer('straight', IDGap, 2, As_bar2, -y1beam+c, 0, y1beam-c, 0)
ops.layer('straight', IDGap, 4, As_bar1, -y1beam+c, z2beam, y1beam-c, z2beam)

print("****************************************","Node","****************************************")
ops.node(1,0,1621)
ops.node(2,0,1600)
ops.node(3,0,410)
ops.node(4,0,320)
ops.node(5,0,200)
ops.node(6,0,0)
ops.node(7,0,-200)
ops.node(8,0,-1200)
ops.node(9,0,-1225)

ops.node(10,200,0)
ops.node(11,260,0)
ops.node(12,440,0)
ops.node(13,500,0)
ops.node(14,2200,0)
ops.node(15,2275,0)

ops.node(16,240+200,410)
ops.node(17,240+200,320)

ops.node(18,240+200,410)
ops.node(19,240+200,320)

ops.fix(9,1,1,0)
ops.fix(15,0,1,0)
print("****************************************","coordTransf","****************************************")
coordTransf = "PDelta"  # Linear, PDelta, Corotational
IDColumnTransf=1
ops.geomTransf(coordTransf, IDColumnTransf)
IDBeamTransf=2
ops.geomTransf(coordTransf, IDBeamTransf)

print("****************************************","beamIntegration","****************************************")
IDFCSIntegration=1
ops.beamIntegration('Trapezoidal', IDFCSIntegration, fiber_column_section,4)
IDFBSIntegration=2
ops.beamIntegration('Trapezoidal', IDFBSIntegration, fiber_beam_section,4)
IDFBGSIntegration=3
ops.beamIntegration('Trapezoidal', IDFBGSIntegration, fiber_beam_gap_section,4)

print("****************************************","Column","****************************************")
ops.element('elasticBeamColumn',1,1,2,Bcol*Hcol,35000,2.133e9,IDColumnTransf)
ops.element('dispBeamColumn', 2, 2, 3,IDColumnTransf,IDFCSIntegration)
ops.element('dispBeamColumn', 3, 3, 4,IDColumnTransf,IDFCSIntegration)
ops.element('dispBeamColumn', 4, 4, 5,IDColumnTransf,IDFCSIntegration)
ops.element('elasticBeamColumn',5,5,6,Bcol*Hcol,35000,2.133e9,IDColumnTransf)
ops.element('elasticBeamColumn',6,6,7,Bcol*Hcol,35000,2.133e9,IDColumnTransf)
ops.element('dispBeamColumn', 7, 7, 8,IDColumnTransf,IDFCSIntegration)
ops.element('elasticBeamColumn',8,8,9,Bcol*Hcol,35000,2.133e9,IDColumnTransf)
print("****************************************","Beam","****************************************")
ops.element('elasticBeamColumn',9,6,10,Bbeam*Hbeam,35000,5.21e8,IDBeamTransf)
ops.element('dispBeamColumn', 10, 10, 11,IDBeamTransf,IDFBGSIntegration)
ops.element('dispBeamColumn', 11, 11, 12,IDBeamTransf,IDFBSIntegration)
ops.element('dispBeamColumn', 12, 12, 13,IDBeamTransf,IDFBSIntegration)
ops.element('dispBeamColumn', 13, 13, 14,IDBeamTransf,IDFBSIntegration)
ops.element('elasticBeamColumn',14,14,15,Bbeam*Hbeam,35000,5.21e8,IDBeamTransf)
ops.equalDOF(11,10,2)
print("****************************************","RigidLink","****************************************")
D=200
ops.element('elasticBeamColumn',15,3,16,3.14*D**2/4,1.e11,3.14*D**4/64,IDColumnTransf)
ops.element('elasticBeamColumn',16,4,17,3.14*D**2/4,1.e11,3.14*D**4/64,IDColumnTransf)
ops.element('elasticBeamColumn',17,12,18,3.14*D**2/4,1.e11,3.14*D**4/64,IDColumnTransf)
ops.element('elasticBeamColumn',18,12,19,3.14*D**2/4,1.e11,3.14*D**4/64,IDColumnTransf)
print("****************************************","PT Strands","****************************************")
ops.element('truss',19,6,14,560,IDPT)
print("****************************************","Damper","****************************************")
ops.element('zeroLength',20,16,18,'-mat',6,6,'-dir',1,2)
ops.element('zeroLength',21,17,19,'-mat',6,6,'-dir',1,2)
opsplt.plot_model("nodes")
print("****************************************","Press","****************************************")
ops.timeSeries('Linear', 11)
ops.pattern('Plain', 100,11)
ops.load(2,0,-9.17e5,0)
ops.constraints("Penalty",1e8,1e8)
ops.numberer("RCM")
ops.system("BandGeneral")
ops.test('NormDispIncr', 1.e-4, 2000)
ops.algorithm("KrylovNewton")
ops.integrator("LoadControl",0.01)
ops.analysis("Static")
ops.analyze(100)
ops.loadConst("-time",0.0)

print("****************************************","Recorder","****************************************")
ops.recorder('Node', '-file', "disp.txt","-time",'-node', 1, '-dof',1, 'disp')
ops.recorder('Node', '-file', "reaction.txt","-time",'-node', 15, '-dof',2, 'reaction')
ops.recorder('Element', '-file', "PT.txt","-time",'-ele',19, 'localForce')
ops.recorder('Element', '-file', "ele20.txt","-time",'-ele', 20, 'localForce')
ops.recorder('Element', '-file', "Dele20.txt","-time",'-ele', 20, 'deformation')
ops.recorder('Element', '-file', "ele21.txt","-time",'-ele', 21, 'localForce')
ops.recorder('Element', '-file', "Dele21.txt","-time",'-ele', 21, 'deformation')
ops.recorder('Element', '-file', "fiber_beam_section.txt","-time",'-ele',10,'section',2, 'fiber',200,125,2,'stressStrain')
ops.recorder('Element', '-file', "fiber_beam_section2.txt","-time",'-ele',10,'section',2, 'fiber',100,100,3,'stressStrain')
print("****************************************","Cycle","****************************************")
ops.timeSeries('Path',22,'-dt',0.1,'-filePath','jz.txt')
ops.pattern( "Plain", 200,22)
#sp $nodeTag $dofTag $dofValue
ops.sp(1,1,1)
ops.test('NormDispIncr',1.e-4, 2000)
ops.integrator("LoadControl",0.005)
ops.analysis("Static")
ops.analyze(8560*2,0.005)