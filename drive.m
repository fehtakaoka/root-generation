% ======= / Script para testes / =======

% Metodos uteis:
%   - Parameters('file','<seu arquivo de parametrossalvo>.mat');
%   - RootStruct/stepGrow();
%   - RootStruct/printRootStruct();
%   - RootStruct/drawRootStruct();
%   - RootStruct/getNodeFromGlbIndex();
%   - Axe/nodeFromIndex();
%   - Axe/printNodeCoords();
%   - Axe/checkGeomConsistency();
%   - Node/getDistance();

%% 

% Adiciona ao path do Matlab todos as subpastas do diretorio atual
addpath(genpath(pwd));

%% Initialization
close all;
clear;
clc;

p = Parameters('file','testegeral.mat');
r = RootStruct(p);

r.stepGrow();
r.stepGrow();
r.stepGrow();
r.stepGrow();
r.stepGrow();
r.stepGrow();
r.stepGrow();
%r.stepGrow();

tap = r.global_lca.initAxis;

r.fill();

figure
r.drawRootStruct(true,true,true);

%% Filling volume process
r.fill();

%% Showing results
figure
r.printRootStruct();
r.drawRootStruct(true,true,true);